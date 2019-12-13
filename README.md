# anki\_plugin\_jaja\_definitions

An Anki add-on, based on the [Japanese Definitions for Korean Vocabulary](https://github.com/steviepoppe/anki_plugin_jk_definitions) add-on (which is based on [Sanseido Definitions](https://ankiweb.net/shared/info/1967553085) add-on), for adding Japanese definitions of Japanese vocabulary. 
It's primarily meant for learners who already had some grasp of Japanese.

The add-on crawls Weblio's dictionary and scrapes the definition for each note. 

\[Add example]

## Bugs and workarounds

It currently doesn't work if only one card is selected, see [bug #9](https://github.com/rgamici/anki_plugin_jaja_definitions/issues/9).
But, it should work if another note or card is selected (it will hide the note fields at the bottom) before clicking on "Regenerate Japanese Definitions."

## Requirements

The add-on requires two fields:

* **Japanese**: the field containing your Japanese expression.
* **JapaneseDefinition**: the field that'll contain the Japanese definitions.

These names can be changed to your liking by opening the `__init__.py` file with a text-editor and editing `expressionField = Japanese'` and `jap_defField = 'JapaneseDefinition'`.
The file can be found in your anki add-ons folder (On linux: `~/local/share/Anki2/addons21/2055037404/`).

## Usage

Just select the cards you'd like to adjust in Anki's Browser and select **Edit** -&gt; **Regenerate Ja-Ja References**. 
Do note that each definition is pulled from Weblio's online dictionary, so if you're bulk-editting thousands of cards, this could take a while.

It currently supports multi-threading, and up to 15 words are searched simultaneously.
This number can be edited on the `__init__.py` file, by searching for `max_threads = 15`.
It doesn't seem to take too much of the CPU resourses, and maybe it can still be increased without problem.
But, be aware that a very high number can trigger the weblio's DDoS protection and crash the results.

For questions or support, please refer to this plugin's [github page](https://github.com/rgamici/anki_plugin_jaja_definitions).
