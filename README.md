# anki\_plugin\_jaja\_definitions

An Anki add-on, based on the [Japanese Definitions for Korean Vocabulary](https://github.com/steviepoppe/anki_plugin_jk_definitions) add-on (which is based on [Sanseido Definitions](https://ankiweb.net/shared/info/1967553085) add-on), for adding Japanese definitions of Japanese vocabulary. 
It's primarily meant for learners who already had some grasp of Japanese.

The add-on crawls Weblio's dictionary and scrapes each definition. 

\[Add example]

## Requirements

The add-on requires two fields:

* **Japanese**: the field containing your Japanese expression.
* **JapaneseDefinition**: the field that'll contain the Japanese definitions.

These names can be changed to your liking by opening the *__init__.py* file with a text-editor and editing `expressionField = Japanese'` and `jap_defField = 'JapaneseDefinition'`.
The file can be found in your anki add-ons folder.

## Usage

Just select the cards you'd like to adjust in Anki's Browser and select **Edit** -&gt; **Regenerate Ja-Ja References**. 
Do note each definition is pulled from Weblio's online dictionary, so if you're bulk-editting thousands of cards, this could take a while.

For questions or support, please refer to this plugin's [github page](https://github.com/steviepoppe/anki_plugin_jk_definitions).
