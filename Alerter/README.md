# Alerter
A simple alert which uses Java 11

## Requirements
- Java 11
- JavaFX SDK 11, which can be downloaded via utility script: `$ ./install.sh`

## Compilation
`$ javac --module-path ./javafx-sdk-11.0.1/lib --add-modules=javafx.controls Alerter.java`

## Usage
```
$ java --module-path ./javafx-sdk-11.0.1/lib --add-modules=javafx.controls Alerter \
--title="Example" --content="Hello world!"
```
