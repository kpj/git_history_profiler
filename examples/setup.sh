wd="$1"

cd "$( dirname "${BASH_SOURCE[0]}" )"
cp -r "./data" "$wd"

mkdir "$wd/results"
