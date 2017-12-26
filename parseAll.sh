rm *.parsed1
rm *.parsed2

for f in *send.log; do 
    mv -- "$f" "${f%.log}.txt"
done

for f in *.log
do
    if [ "$f" != "automate.log" ]; then
        echo "$f"
        python3 log_file_parser.py "$f" "$f.parsed1"
        python3 log_json_summary.py "$f.parsed1" "$f.parsed2"
    fi
done