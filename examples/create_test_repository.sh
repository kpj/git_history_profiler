set -e -u


# setup directory
repo_dir="$1"
rm -rf "$repo_dir"
mkdir -p "$repo_dir"
cd "$repo_dir"

# setup repository
git init
touch pipeline.sh
git add pipeline.sh

# add commits
cat <<\EOF > pipeline.sh
data_dir="./data"
cat "$data_dir/input.csv" > results/output.csv
echo "2,baz" >> results/output.csv
EOF
chmod +x pipeline.sh
git commit -am"Initial commit"

cat <<\EOF > pipeline.sh
data_dir="./data"
cat "$data_dir/input.csv" > results/output.csv
sleep 2
echo "2,bazZ" >> results/output.csv
EOF
chmod +x pipeline.sh
git commit -am"Introduce error and delay"

cat <<\EOF > pipeline.sh
data_dir="./data"
cat "$data_dir/input.csv" > results/output.csv
sleep 1.3
echo "2,baz" >> results/output.csv
EOF
chmod +x pipeline.sh
git commit -am"Fix error"
