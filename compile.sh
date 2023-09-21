echo compiling java sources...
rm -rf class
mkdir class

javac -cp "./libs/commons-math3-3.6.1.jar" -d class $(find ./src -name *.java)

echo make jar archive
cd class
jar cf brainimage-1.0.jar ./
rm ../brainimage-1.0.jar
mv brainimage-1.0.jar ../
cd ..
rm -rf class

echo done.
