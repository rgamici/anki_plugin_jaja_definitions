# anki_plugin_jaja_definitions

An Anki add-on, based on the <a href="https://ankiweb.net/shared/info/1967553085" rel="nofollow">Sanseido Definitions</a> add-on, for adding Japanese translations of Korean vocabulary. It's primarily meant for Korean learners who're proficient in or simultaneously learning, Japanese.

The add-on crawls Weblio's Korean-Japanese dictionary and scrapes each translation. As 개 could mean either dog, or be used as a particular counter, the field containing the Japanese definitions will look like this:

* (1) 犬
* (2) 個 

## Requirements

The add-on requires two fields:

<ul>
<li>**Korean**: the field containing your Korean expression.</li>
<li>**Japanese**: the field that'll contain the Japanese translations.</li>
</ul>

These names can be changed to your liking by opening the *JapaneseDefinitionsKoreanVoc.py* file with a text-editor and editting `expressionField = 'Korean'` and `jap_transField = 'Japanese'. The file can be found in your anki add-ons folder.

## Usage

Just select the cards you'd like to adjust in Anki's Browser and select **Edit** -&gt; **Regenerate JK References**. Do note each definition is pulled from Weblio's online dictionary, so if you're bulk-editting thousands of cards, this could take a while.

For questions or support, please refer to this plugin's <a href="https://github.com/steviepoppe/anki_plugin_jk_definitions" rel="nofollow">github page</a>.
