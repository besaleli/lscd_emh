CORPUSDIR=parsed_corpus

mkdir -p $CORPUSDIR

python3 corpus/get_raw_sents.py --corpus $CORPUSDIR --jemh corpora
# python3 get_embeddings.py --server $SERVER_URL --corpus $CORPUSDIR
