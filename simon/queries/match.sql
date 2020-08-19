drop table if exists query_match;
create temporary table if not exists query_match (
	name_id integer,
	word_position integer,
	query_word_position integer,

	displacement_sum integer,
	displacement_count integer,
	score integer,

	-- used for counting the amount of matches between word <-> query.
	unique (name_id, word_position, query_word_position)
);

insert or ignore
into query_match
select
	name_bigram.name_id,
	name_bigram.word_position,
	query.word_position as query_word_position,
	abs(name_bigram.word_bigram_position -
		query.word_bigram_position
	) as displacement_sum,
	1 as displacement_count,
	1 as score
from query
inner join bigram using(bigram)
inner join name_bigram on name_bigram.bigram_id = bigram.id
where bigram.language = 1 -- in (3, 2, 1)
order by abs(name_bigram.word_bigram_position - query.word_bigram_position)
on conflict (name_id, word_position, query_word_position)
do update set
	displacement_sum = displacement_sum + excluded.displacement_sum,
	displacement_count = displacement_count + 1,
	score = score + 1;

--> 160 ms (language en = 1)
--> 180 ms, VPS: 40ms


drop table if exists word_match;
create temporary table if not exists word_match (
	name_id integer,
	query_word_position integer,

	displacement integer,
	score integer,

	unique (name_id, query_word_position)
);

INSERT OR IGNORE
INTO word_match
SELECT
	name_id,
	query_word_position,
	displacement_sum / displacement_count AS displacement,
	score
FROM query_match
WHERE score > 1 OR (SELECT bigrams FROM query_meta) <= 4 -- try other values
ORDER BY score DESC, displacement;

--> 100 ms (=> 260 ms)
--> 40  ms (=> 220 ms), VPS: 0 ms (=> 40ms)


/**/

SELECT
	name_id, name,
	AVG(displacement) AS avg_displacement,
	MAX(displacement) AS max_displacement,
	MIN(displacement) AS min_displacement,
	MIN(query_word_position) AS min_query_word,
	SUM(score) AS score
FROM word_match
INNER JOIN name ON name_id = name.id
-- WHERE name_id IN (8789, 2553)
GROUP BY name_id
ORDER BY
	score DESC,
	avg_displacement,
	max_displacement,
	min_displacement,
	min_query_word
LIMIT 1;

--> local: => 80ms
--> VPS: => 40ms

/**/




/*/

SELECT
	name_id,
	name,
	word_position,
	query_word_position,
	query_match.score,
	query_match.displacement,
	query_match.displacement_count,
	(	COUNT(DISTINCT word_position) -
		COUNT(DISTINCT query_word_position)
	) AS word_variance
FROM query_match
INNER JOIN name ON name_id = name.id
WHERE name_id IN (
	8789, 	-- Nirvana High Paladin
--	31481,	-- Hoher Nirvana-Paladin
	2553	-- Fire King High Avatar Garunix
)
GROUP BY name_id
ORDER BY name_id

/**/






/*
	WHERE name_id IN (
		7,
		8789, 	-- Nirvana High Paladin
	--	31481,	-- Hoher Nirvana-Paladin
		2553	-- Fire King High Avatar Garunix
	)


	-- MIN(displacement_sum / displacement_count) OVER w AS displacement,
	-- MAX(score) OVER w AS score
	-- WINDOW w AS ( PARTITION BY name_id, query_word_position )


	COALESCE((
		SELECT score
		FROM query_match
		WHERE
			name_id = name_bigram.name_id AND
			word_position = name_bigram.word_position AND
			query_word_position = query.word_position
	), 0) + 1 as score
*/
