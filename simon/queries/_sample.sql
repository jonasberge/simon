DROP TABLE IF EXISTS "query";
DROP TABLE IF EXISTS "query_meta";

CREATE TEMPORARY TABLE "query" (
	"word_position" INTEGER NOT NULL,
	"word_bigram_position" INTEGER NOT NULL,
	"bigram" VARCHAR(2) NOT NULL
);

CREATE TEMPORARY TABLE "query_meta" (
	"words" INTEGER NOT NULL,
	"bigrams" INTEGER NOT NULL
);

DROP INDEX IF EXISTS idx_query_bigram;
DROP INDEX IF EXISTS idx_query_positions;

CREATE INDEX idx_query_positions ON query(word_position, word_bigram_position);
CREATE INDEX idx_query_bigram ON query(bigram);


-- nirvana high
INSERT INTO query (word_position, word_bigram_position, bigram)
VALUES
	(0, 0, 'ni'),
	(0, 1, 'ir'),
	(0, 2, 'rv'),
	(0, 3, 'va'),
	(0, 4, 'an'),
	(0, 5, 'na'),

	(1, 0, 'hi'),
	(1, 1, 'ig'),
	(1, 2, 'gh');


INSERT INTO query_meta
VALUES (
	(SELECT COUNT(DISTINCT word_position) FROM query),
	(SELECT SUM(1) FROM query)
);

SELECT * FROM query_meta;
