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

export class Query {
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

/**
 * @param {SearchResult[]} results
 */
function sortResults(results) {
    /**
     * @param {Match[]} a
     * @param {Match[]} b
     */
    function mi(a, b) {
        if (a.length == 0) {
            if (b.length == 0) return 0;
            return 100;
        }
        if (b.length == 0) return -100;

        if (a[0].start == 0) {
            if (b[0].start == 0) return 0;
            return -1;
        }
        if (b[0].start == 0) return 1;
        return 0;
    }

    return results.sort((a, b) => {
        let cmp = mi(a.titleMatches, b.titleMatches);

        if (cmp == 0) return a.entry.title.localeCompare(b.entry.title);
        return cmp;
    });
}

/**
 * @param {string} q
 */
export function makeQuery(q) {
    // Split into non-empty search terms
    const terms = new Set(q.split(" "));
    terms.delete("");
    return new Query(Array.from(terms));
}

export class Searcher {
    /**
     * @param {Array<Entry>} entries
     */
    constructor(entries) {
        this.entries = entries;
        this.cache = [];
        this.lastQuery = new Query([]);
    }

    /**
     * @param {Query} query
     */
    search(query) {
        if (!query.terms.length) return [];

        let results = searchEntries(query, this.entries);
        results = sortResults(results);

        this.cache = results;
        this.lastQuery = query;
        return results;
    }
}