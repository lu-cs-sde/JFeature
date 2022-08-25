#!/bin/zsh
#This script will trigger the entire evaluation process.

# Function that logs an error message
function log_error() {
   echo "\u001b[31;1m[ERROR]\e[1;37m $err \u001b[0m"
}

# Function that logs an info message
function log_info() {
   echo "\u001b[33;1m[INFO]\e[1;37m $info \u001b[0m"
}

# Function that logs a success message
function log_success() {
   echo "\u001b[32;1m[SUCCESS]\e[1;37m $success \u001b[0m"
}

if [[ $(uname) != "Darwin" ]]; then
   alias gdate="date"
fi

#Checking if the correct number of arguments are passed.
if [ "$#" -le 0 ]; then
   err="Not enough arguments passed. Please pass the following arguments:\
   \n\t1. true/false/only: download repositories. Only will download the repositories"
   log_error
   exit 1
fi

if [ "$1" != "true" ] && [ "$1" != "only" ] && [ "$1" != "false" ]; then
   err="The argument must be true, false or only."
   log_error
   exit 1
fi

# Static array with all IntraJ aliases.
declare -a INTRAJ_ALIASES=(intraj_bl.jar intraj_daa.jar intraj_npa.jar intraj_cfgnpa.jar intraj_cfg.jar intraj_cfgdaa.jar intraj_daanpa.jar)

info="SETTING ENVIRONMENT VARIABLES"
log_info

. ~/.sdkman/bin/sdkman-init.sh
sdk use java 8.0.275.fx-zulu
set -e

N_ITER=1
N_ITER_SS=1
CHECKOUT=$1
TYPE_OF_EVAL="inspector"

read_dom() {
   local IFS=\>
   read -d \< ENTITY CONTENT
   local ret=$?
   TAG_NAME=${ENTITY%% *}
   ATTRIBUTES=${ENTITY#* }
   return $ret
}

# The results of the evaluation are stored in a directory named with a timestamp.
# The timestamp is used to avoid overwriting previous results.
TIMESTAMP=$(date +%Y%m%d%H%M%S)
EVAL_DIR=results/$TIMESTAMP
mkdir -p $EVAL_DIR

prj_json="projects.json"

count=$(jq '.benchmarks | length' $prj_json)
for ((i = 0; i < $count; i++)); do
   enable=$(jq -r ".benchmarks[$i].enable" $prj_json)

   if [ "$enable" = "false" ]; then
      #Skipping the banchmark if not enabled
      continue
   fi
   name=$(jq -r '.benchmarks['$i'].name' $prj_json)
   # IF CHECKOUT == TRUE OR CHECKOUT == ONLY, then download the repositories.
   if [ "$CHECKOUT" = "true" ] || [ "$CHECKOUT" = "only" ]; then
      rm -r -f $name #remove the previous banchmark folder
      # checkout the benchmarks using the appropriate checkout method.
      url=$(jq -r '.benchmarks['$i'].url' $prj_json)
      checkout=$(jq -r '.benchmarks['$i'].checkout' $prj_json)
      info="CHECKING OUT $name"
      log_info
      if [ "$checkout" = "wget" ]; then
         wget $url
         tar -xzf $(basename $url)
         rm $(basename $url)
      elif [ "$checkout" = "svn" ]; then
         commit=$(jq -r '.benchmarks['$i'].commit' $prj_json)
         svn checkout $url@$commit $name
         # if [ "$commit" != "null" ]; then # if commit is not specified, use the latest commit
         #    post_checkout=$(jq -r '.benchmarks['$i'].post_checkout' $prj_json)
         #    post_checkout_note=$(jq -r '.benchmarks['$i'].post_checkout_note' $prj_json)
         #    cd $name
         #    git checkout $commit
         #    # if post_checkout is specified, execute the command
         #    # e.g., git submodule update --init --recursive
         #    # Is always followed by a note explaining why the post_checkout is done.
         #    if [ "$post_checkout" != "null" ]; then
         #       info="$post_checkout_note"
         #       log_info
         #       git apply <$post_checkout
         #    fi
         #    cd ..
         # fi
      elif [ "$checkout" = "git" ]; then
         commit=$(jq -r '.benchmarks['$i'].commit' $prj_json)
         git clone $url $name
         if [ "$commit" != "null" ]; then # if commit is not specified, use the latest commit
            post_checkout=$(jq -r '.benchmarks['$i'].post_checkout' $prj_json)
            post_checkout_note=$(jq -r '.benchmarks['$i'].post_checkout_note' $prj_json)
            cd $name
            git checkout $commit
            # if post_checkout is specified, execute the command
            # e.g., git submodule update --init --recursive
            # Is always followed by a note explaining why the post_checkout is done.
            if [ "$post_checkout" != "null" ]; then
               info="$post_checkout_note"
               log_info
               git apply <$post_checkout
            fi
            cd ..
         fi
      else
         err="Checkout method not supported"
         log_error
         exit 1
      fi
      #  if only stop here
      if [ "$CHECKOUT" = "only" ]; then
         continue
      fi
   fi
   dir_to_analyze=$(jq -r '.benchmarks['$i'].dir_to_analyze' $prj_json)
   all_files=($name/$dir_to_analyze**/*.java)
   # Removing from all_files all files that are directories and saveit in a new variable
   all_files_no_dir=()
   for file in "${all_files[@]}"; do
      if [ -d "$file" ]; then
         continue
      else
         all_files_no_dir+=($file)
      fi
   done
   all_files=("${all_files_no_dir[@]}")

   exclude_dirs=$(jq -r '.benchmarks['$i'].exclude_dirs' $prj_json)
   # Declaring array of pdf names
   pdf_names=()
   if [ "$exclude_dirs" != "null" ]; then
      count_dirs=$(jq -r '.benchmarks['$i'].exclude_dirs | length' $prj_json)
      # exclude_dirs is a JSON array containg pairs of directory to exclude and the reason for excluding it.
      # e.g., [["/tmp", "For some reason"], ["/home", "For some other reason"]]
      for ((j = 0; j < $count_dirs; j++)); do
         dir=$(jq -r '.benchmarks['$i'].exclude_dirs['$j'].path' $prj_json)
         reason=$(jq -r '.benchmarks['$i'].exclude_dirs['$j'].motivation' $prj_json)
         info="Excluding '$dir' because: $reason"
         log_info
         # removing files from $all_files that starts with $dir
         for file in ${all_files[@]}; do
            if [[ $file == $name/$dir* ]]; then
               all_files=("${all_files[@]/$file/}")
               info="Excluding $file"
               log_info
            fi
         done
      done
   fi
   # Run the evaluation process.
   classpath=$(jq -r '.benchmarks['$i'].classpath' $prj_json)

   hasclasspath=$(jq -r '.benchmarks['$i'].hasclasspath' $prj_json)
   if [ "$hasclasspath" = "true" ]; then
      cd $name
      # check if .classpath exists
      if [ -f .classpath ]; then
         while read_dom; do
            if [ "$TAG_NAME" = "classpathentry" ]; then

               # Remove everything in Attribute until the first space
               ATTRIBUTES=${ATTRIBUTES#* }
               # Remove the prefix 'path="'
               ATTRIBUTES=${ATTRIBUTES#*path=\"}
               #remove the suffix '"'
               ATTRIBUTES=${ATTRIBUTES%\"*}
               # Append current directory to Attributes
               classpath=$classpath:$(pwd)/$ATTRIBUTES
            fi
         done <.classpath
         classpath=$classpath

      fi
      cd ..
   fi

   info="RUNNING BENCHMARK ON PROJECT $name"
   log_info
   info="CLASSPATH: $classpath"
   log_info
   info="DIR_TO_ANALYZE: $dir_to_analyze"
   log_info
   folder=$name
   iter=0
   if [[ "$TYPE_OF_EVAL" = "inspector" ]]; then
      java -Xss8192M -Xms128g -jar ../fe.jar -classpath $classpath $all_files -prjname=$name  2> /dev/null || true
      mv $name"features.csv" $EVAL_DIR
      info="Plotting the results $name"
      log_info
      python3 plots.py $EVAL_DIR/$name"features.csv" $name
      cloc $all_files
   elif [[ "$TYPE_OF_EVAL" = "pasta" ]]; then
      java -jar pasta-server.jar ../../../../tools/extendj/java8/extendj.jar -classpath $classpath -nowarn
   elif [[ "$TYPE_OF_EVAL" = "inspectorhistory" ]]; then
      # iterate over all commit in master branch
      cd $folder
      for commit in $(git rev-list --all); do
         # Checking if skip_versions is not null
         skip_versions=$(jq -r '.benchmarks['$i'].skip_version' ../$prj_json)
         if [ "$skip_versions" != "null" ]; then
            # iterate over all skip_versions
            for ((j = 0; j < $(jq -r '.benchmarks['$i'].skip_version | length' ../$prj_json); j++)); do
               skip_version=$(jq -r '.benchmarks['$i'].skip_version['$j']' ../$prj_json)
               if [ "$skip_version" = "$commit" ]; then
                  info="Skipping commit $commit"
                  log_info
                  continue 2
               fi
            done
         fi

         cd ..
         info="Running inspector on commit $commit"
         log_info
         echo $(pwd)
         cd $folder
         echo $(pwd)
         git checkout $commit
         cd ..
         all_files=($folder/$dir_to_analyze**/*.java)
         # Removing from all_files all files that are directories
         for file in ${all_files[@]}; do
            if [ -d $file ]; then
               all_files=("${all_files[@]/$file/}")
            fi
         done
         name=$folder"_"$iter"_"$commit
         java -Xss1024M -jar ../fe.jar -classpath $classpath $all_files -prjname=$name
         mv $name"features.csv" $EVAL_DIR
         info="Plotting the results $name"
         log_info
         python3 plots.py $EVAL_DIR/$name"features.csv" $name
         # Add the pdf to the pdf_names array
         convert -density 400 $EVAL_DIR/$name"_merged.pdf" $EVAL_DIR/$iter".png"
         pdf_names+=($EVAL_DIR/$name"_"$iter"_"$commit"_merged.png")
         cd $folder
         iter=$((iter + 1))
      done
   elif [[ "$TYPE_OF_EVAL" = "javac" ]]; then
      javac -cp $classpath ${all_files[@]}
   elif [[ "$TYPE_OF_EVAL" = "extendj" ]]; then
      java -jar ../extendj.jar -classpath $classpath $all_files -nowarn
   elif [[ "$TYPE_OF_EVAL" = "eval" ]]; then
      elapsed=1
      # iterate over all INTRAJ_ALIASES and run the evaluation
      for alias in "${INTRAJ_ALIASES[@]}"; do

         intraj=$alias
         # Removes the .jar at the end
         readable_name=${intraj%.*}
         info="RUNNING BENCHMARK ON PROJECT $name WITH $readable_name"
         log_info
         eval_warmup
         info="$results"
         log_info
         # saving the results in a file
         echo $readable_name >>$EVAL_DIR/$name"_"$readable_name"_warmup_results.new"
         echo "$results" >>$EVAL_DIR/$name"_"$readable_name"_warmup_results.new"
         eval_steady
         info="$results"
         log_info
         echo $readable_name >>$EVAL_DIR/$name"_"$readable_name"_steady_results.new"
         echo "$results" >>$EVAL_DIR/$name"_"$readable_name"_steady_results.new"

         #######################################################################

         # Running the same evaluation on the old jars
         info="RUNNING BENCHMARK ON PROJECT $name WITH old/$intraj"
         log_info

         intraj=old_jars/$alias
         info="RUNNING BENCHMARK ON PROJECT $name WITH $intraj"
         log_info
         eval_warmup
         info="$results"
         log_info
         # saving the results in a file
         echo $readable_name >>$EVAL_DIR/$name"_"$readable_name"_warmup_results.old"
         echo "$results" >>$EVAL_DIR/$name"_"$readable_name"_warmup_results.old"
         eval_steady
         info="$results"
         log_info
         echo $readable_name >>$EVAL_DIR/$name"_"$readable_name"_steady_results.old"
         echo "$results" >>$EVAL_DIR/$name"_"$readable_name"_steady_results.old"

      done
      info="Plotting the results"
      log_info
      python3 performance.py $EVAL_DIR $name
   else
      err="Type of evaluation not supported"
      log_error
      exit 1
   fi
   # ffmpeg -r 1/10 -i *merged.png -c:v libx264 -r 30 -pix_fmt yuv420p video.mp4
   # TODO: Add the other types of evaluation.
done
