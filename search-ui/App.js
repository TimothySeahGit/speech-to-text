// modified from https://www.elastic.co/guide/en/search-ui/current/tutorials-elasticsearch.html

import React from "react";

// import AppSearchAPIConnector from "@elastic/search-ui-app-search-connector";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
    ErrorBoundary,
    Facet,
    SearchProvider,
    SearchBox,
    Results,
    PagingInfo,
    ResultsPerPage,
    Paging,
    Sorting,
    WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

// import {
//     buildAutocompleteQueryConfig,
//     buildFacetConfigFromConfig,
//     buildSearchOptionsFromConfig,
//     buildSortOptionsFromConfig,
//     getConfig,
//     getFacetFields
// } from "./config/config-helper";

const connector = new ElasticsearchAPIConnector({
    host: "http://localhost:9200", // The browser can only see containers from the outside!
    // host: "http://speech-to-text-elastic-backend-1:9200", # so, this is only for prod.
    index: "cv-transcriptions-float"
});

// const config = {
//     searchQuery: {
//         facets: buildFacetConfigFromConfig(),
//         ...buildSearchOptionsFromConfig()
//     },
//     autocompleteQuery: buildAutocompleteQueryConfig(),
//     apiConnector: connector,
//     alwaysSearchOnInitialLoad: true
// };
const config = {
    searchQuery: {
        search_fields: {
            title: {
                weight: 3
            },
            generated_text: {},
            age: {},
            gender: {},
            accent: {}
        },
        result_fields: {
            generated_text: {},
            duration: {},
            age: {},
            gender: {},
            accent: {}
        },
        disjunctiveFacets: ["age.keyword", "gender.keyword", "accent.keyword"],
        facets: {
            "duration": {
                type: "range",
                ranges: [
                    { "to": 2, "name": "Less than 2 seconds" },
                    { "from": 2.01, "to": 5, "name": "2 to 5 seconds" },
                    { "from": 5.01, "to": 10, "name": "5 to 10 seconds" },
                    { "from": 10.01, "name": "More than 10 seconds" }
                ]
            },
            "age.keyword": { type: "value" },
            "gender.keyword": { type: "value" },
            "accent.keyword": { type: "value" },
        }
    },
    autocompleteQuery: {
        results: {
            resultsPerPage: 5,
            search_fields: {
                "generated_text": {
                    weight: 3
                }
            },
            result_fields: {
                generated_text: {
                    snippet: {
                        size: 100,
                        fallback: true
                    }
                },
                filename: {
                    raw: {}
                }
            }
        },
        suggestions: {
            types: {
                results: { fields: ["generated_text"] }
            },
            size: 4
        }
    },
    apiConnector: connector,
    alwaysSearchOnInitialLoad: true
};

export default function App() {
    return (
        <SearchProvider config={config}>
            <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
                {({ wasSearched }) => {
                    return (
                        <div className="App">
                            <ErrorBoundary>
                                <Layout
                                    header={
                                        <SearchBox
                                            autocompleteMinimumCharacters={3}
                                            autocompleteResults={{
                                                linkTarget: "_blank",
                                                sectionTitle: "Results",
                                                titleField: "title",
                                                urlField: "url",
                                                shouldTrackClickThrough: true
                                            }}
                                            autocompleteSuggestions={false}
                                            debounceLength={0}
                                        />
                                    }
                                    sideContent={
                                        <div>
                                            {wasSearched && <Sorting label={"Sort by"} sortOptions={[]} />}
                                            <Facet key={"1"} field={"duration"} label={"duration"} />
                                            <Facet key={"2"} field={"age.keyword"} label={"age"} />
                                            <Facet key={"3"} field={"gender.keyword"} label={"gender"} />
                                            <Facet key={"4"} field={"accent.keyword"} label={"accent"} />
                                        </div>
                                    }
                                    bodyContent={<Results shouldTrackClickThrough={true} />}
                                    bodyHeader={
                                        <React.Fragment>
                                            {wasSearched && <PagingInfo />}
                                            {wasSearched && <ResultsPerPage />}
                                        </React.Fragment>
                                    }
                                    bodyFooter={<Paging />}
                                />
                            </ErrorBoundary>
                        </div>
                    );
                }}
            </WithSearch>
        </SearchProvider>
    );
}