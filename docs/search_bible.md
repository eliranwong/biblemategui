# Bible Search Modes

## Search References

Enter verse references or words for searches.

## Search Words

Three different modes are supported for word searches:

1. Literal search for plain text

e.g. Enter plain text, like:

> In the beginning

2. Search for a regular expression pattern

e.g. To search for verses that contain either `love`, `hope`, or `faith`

> love|hope|faith

e.g. To search for verses that contain either `love`, `hope`, and `faith`

> ^(?=.*\blove\b)(?=.*\bhope\b)(?=.*\bfaith\b).*

e.g. To search for words in specific word

> Naomi.*?Ruth

3. Semantic search for meaning

e.g. To search for an idea or similar words

> David fled

Adjust the `Similar Verses` number in preferences, to set the maximum number of similar verses to be displayed.

## Case-sentivitiy

There is a checkbox to toggle support of case-sensitive searches.  This option applies to `literal` and `regex` modes only.

## Search Scope

Select from the book dropdown list, to limit the search scope for a search.

## Search Multiple Bibles

Select multiple bibles from the bible dropdown list to perform searches in multiples bibles.

If no bible is slected, the app searches the opened bible in the active bible area tab.