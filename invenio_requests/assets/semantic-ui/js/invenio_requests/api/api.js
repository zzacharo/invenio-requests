import { http } from "./config";

export class RequestLinkExtractor {
  #links;

  constructor(requestLinks) {
    if (!requestLinks) {
      throw TypeError("Request resource links are undefined");
    }
    this.#links = requestLinks;
  }

  get timeline() {
    if (!this.#links.timeline) {
      throw TypeError("Timeline link missing from resource.");
    }
    return this.#links.timeline;
  }

  get comments() {
    if (!this.#links.comments) {
      throw TypeError("Comments link missing from resource.");
    }
    return this.#links.comments;
  }

  get actions() {
    if (!this.#links.actions) {
      throw TypeError("Actions link missing from resource.");
    }
    return this.#links.actions;
  }
}

export class InvenioRequestsTimelineAPI {
  #links;
  constructor(requestLinkExtractor) {
    this.#links = requestLinkExtractor;
  }

  getTimeline = async (params) => {
    return await http.get(this.#links.timeline, { params });
  };

  submitComment = async (payload) => {
    return await http.post(this.#links.comments, payload);
  };
}

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

export class RequestEventsApi {
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
