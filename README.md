# anki\_plugin\_jaja\_definitions

An Anki add-on, based on the [Japanese Definitions for Korean Vocabulary](https://github.com/steviepoppe/anki_plugin_jk_definitions) add-on (which is based on [Sanseido Definitions](https://ankiweb.net/shared/info/1967553085) add-on), for adding Japanese definitions of Japanese vocabulary. 
It's primarily meant for learners who already had some grasp of Japanese.

This add-on crawls Weblio's dictionary and scrapes the definition for each selected note. 
It also does a simple cleaning on the fetched definition to remove some useless  text from weblio, for example the word's pronunciation and some external links.
If you find any problem with the scraped definition, open an [issue on github](https://github.com/rgamici/anki_plugin_jaja_definitions/issues), please mention which word resulted in the undesired results.

\[Add example]

## Bugs and workarounds

~~It currently doesn't work if only one card is selected, see [bug #9](https://github.com/rgamici/anki_plugin_jaja_definitions/issues/9).
But, it should work if another note or card is selected (it will hide the note fields at the bottom) before clicking on "Regenerate Japanese Definitions."~~  
**Fixed**.
Now, it works if a single card is selected.

## Requirements

The add-on requires two fields:

* **Japanese**: the field containing your Japanese expressions.
* **JapaneseDefinition**: the field that'll receive the Japanese definitions.

If you want to use different names to match your current note types, you can edit those values on Tools > Add-ons > Config.
You need to restart Anki for the changes take effect.

## Usage

Just select the card(s) you'd like to adjust in Anki's Browser and select **Edit** -&gt; **Regenerate Japanese definitions**. 
Do note that each definition is pulled from Weblio's online dictionary, so if you're bulk-editting thousands of cards, this could take a while.

It currently supports multi-threading, and by default up to 15 words are searched simultaneously.
This value can be changed on Tools > Add-ons > Config, it is not necessary to restart Anki for the changes take effect.
It doesn't seem to take too much of the CPU resources, and maybe it can still be increased depending on your PC processing power.
But, be aware that a very high number can trigger weblio's DDoS protection and crash the results.

For questions or support, please refer to this plugin's [github page](https://github.com/rgamici/anki_plugin_jaja_definitions).
