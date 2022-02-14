import {
  http
} from './config';

export class RequestEventsLinkExtractor {
  #links;
  constructor(links) {
    this.#links = links;
  }

  get eventUrl() {
    if (!this.#links.self) {
      throw TypeError("Self link missing from resource.");
    }
    return this.#links.self;
  }
}

export class InvenioRequestEventsApi {
  #links;
  constructor(links) {
    this.#links = links;
  }

  getComment = async () => {
    return await http.get(this.#links.eventUrl);
  };

  updateComment = async (payload) => {
    return http.put(this.#links.eventUrl, payload);
  };

  deleteComment = async () => {
    return await http.delete(this.#links.eventUrl);
  };
}

export class QueryBuilder {
  #query = {};

  constructor(query) {
    this.#query = query;
  }

  #queryMethodFactory = (property, query, value) => {
    if (!value) {
      throw TypeError(`no ${property} value passed`);
    }

    query[property] = value;

    return new QueryBuilder(query);
  };

  setSort = (value) => this.#queryMethodFactory("sort", this.#query, value);

  setSize = (value) => this.#queryMethodFactory("size", this.#query, value);

  setPage = (value) => this.#queryMethodFactory("page", this.#query, value);

  get = () => this.#query;
}
