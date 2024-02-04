# Rename all *.txt to *.text
for file in *.jpg; do
    mv -- "$file" "${file%.jpg}.jpeg"
done