# RapML
Compiles a rap lines dataset - dataset scraped from rapgenius and built using scripts in "Data" folder. Uses seq2seq LSTM to generate **fire bars** after being given an input line of rap lyrics.

The model is trained by feeding one line of lyrics as inputs, with a matching output sentence that is ideally, on-topic & rhymes.

### Status
The current version of the model generates structured nonsense. But there are a few mods required that would really improve its performance. 

### Examples
A couple of less offensive generated lyric excerpts are shown below:

**[INPUT]** *i told y'all about that fake love*

**[RapML]**  *but if they up the whole screamin' i movin' with this one*

Doesn't make sense, but it at least rhymes.

**[INPUT]** *his palms are sweaty, knees weak, arms are heavy* 

**[RapML]** *on the black of every of old bentley*

Again, nonsense, but it rhymes.
