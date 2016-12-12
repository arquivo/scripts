#!/bin/bash
# Script to execute the final steps to index a collection for PWA (sort and prunning)
. /opt/searcher/scripts/functions

hadoop="${HADOOP_HOME}/bin/hadoop"
get_time="/usr/bin/time -a -o report-phase2"


COLLECTION_NAME=$1
COLLECTION_FOLDER=${COLLECTION_FOLDER:-"/data/collection_data"}

cd "$COLLECTION_FOLDER/$COLLECTION_NAME"

echo $COLLECTION_NAME

outputs="outputs_$COLLECTION_NAME"
dest_folder="/data/$COLLECTION_NAME/$outputs"

echo $dest_folder

check_file_exists ~/.indexing
. ~/.indexing

 # Sort the index
sort_indexes(){
     echo -e "IndexSorter\n$(date)" >> 'time-phase2'
     $get_time -f "*Time to sort index, %E seconds" ${HADOOP_HOME}/bin/hadoop jar ${SCRIPTS_DIR}/nutchwax-job-0.11.0-SNAPSHOT.jar class org.apache.nutch.indexer.IndexSorterArquivoWeb $dest_folder
     correct $? "There was an error inverting index"
     mv $dest_folder/index $dest_folder/index-orig
     correct $? "There was an error moving original index to new directory"
     mv $dest_folder/index-sorted $dest_folder/index
     correct $? "There was an error moving inverted index to index directory"
     date >> "time-phase2"
}

# Index prunning
index_prunning(){
    INDEX_DIR="${dest_folder}/index"
        INDEX_DIR_OUT="${dest_folder}/index-prunning"
        echo -e "PruningIndexes\n$(date)" >>"time-phase2"
        $get_time -f "*Time prunning index, %E seconds" java -Xmx60000m -classpath ${SCRIPTS_DIR}/lib/pwalucene-1.0.0-SNAPSHOT.jar org.apache.lucene.pruning.PruningTool -impl arquivo -in $INDEX_DIR -out $INDEX_DIR_OUT -del pagerank:pPsv,outlinks:pPsv -t 1
        correct $? "There was an error in prunning index process"
        mv $INDEX_DIR "$INDEX_DIR-sorted"
        correct $? "There was an error moving sorted index to new directory"
        mv $INDEX_DIR_OUT $INDEX_DIR
        correct $? "There was an error moving prunning index to index directory"
        date >> "time-phase2"
}

# Copy stop words
copy_stopwords(){
    cp "${SCRIPTS_DIR}/stopwords.cache" "${dest_folder}/index/stopwords.cache"
}

sort_indexes
index_prunning
copy_stopwords

