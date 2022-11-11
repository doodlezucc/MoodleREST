class Match {
    /**
     * @param {number} start
     * @param {number} end
     */
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }
}

class SearchResult {
    /**
     * @param {Entry} entry
     * @param {Array<Match>} titleMatches
     * @param {Array<Match>} textMatches
     */
    constructor(entry, titleMatches, textMatches) {
        this.entry = entry;
        this.titleMatches = titleMatches;
        this.textMatches = textMatches;
    }
}

export class Entry {
    /**
     * @param {string} title
     * @param {string} text
     */
    constructor(title, text) {
        this.title = title;
        this.text = text;
    }
}

/**
 * @param {string} s
 */
function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

class Query {
    /**
     * @param {Array<string>} terms
     */
    constructor(terms) {
        this.terms = terms;
        this.regex = new RegExp(this.terms.map(escapeRegExp).join("|"), "gmi");
    }
}

/**
 * @param {string} s
 * @param {Query} query
 */
function match(s, query) {
    const results = [];
    for (const m of s.matchAll(query.regex)) {
        results.push(new Match(m.index, m.index + m[0].length));
    }
    return results;
}

/**
 * @param {Query} query
 * @param {Entry} entry
 */
function searchSingle(query, entry) {
    const m1 = match(entry.title, query);
    const m2 = match(entry.text, query);
    if (!m1.length && !m2.length) return null;

    return new SearchResult(entry, m1, m2);
}

/**
 * @param {string} query
 * @param {Iterable<Entry>} entries
 * @returns {Array<SearchResult>}
 */
function searchEntries(query, entries) {
    const results = [];
    for (const entry of entries) {
        const res = searchSingle(query, entry);
        if (res) results.push(res);
    }
    return results;
}

export class Searcher {
    /**
     * @param {Array<Entry>} entries
     */
    constructor(entries) {
        this.entries = entries;
        this.cache = [];
        this.lastQuery = "";
    }

    /**
     * @param {string} q
     */
    search(q) {
        // Split into non-empty search terms
        const terms = new Set(q.split(" "));
        terms.delete("");
        const query = new Query(Array.from(terms));
        if (!query.terms.length) return [];

        const results = searchEntries(query, this.entries);

        this.cache = results;
        this.lastQuery = q;
        return results;
    }
}