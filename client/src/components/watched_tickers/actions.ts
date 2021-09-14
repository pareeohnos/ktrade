import WatchedTicker from "@/data/models/watched-ticker";
import axios from "axios";

export const buy = (watched: WatchedTicker): Promise<WatchedTicker> => {
  return axios.post("/trades", {
    ticker: watched.ticker
  }).then(({ data }) => data);
};

export const unwatch = (watched: WatchedTicker): Promise<WatchedTicker> => {
  const confirmed = confirm("Are you sure?");
  if (confirmed) {
    return axios.post("/unwatch", {
      ticker: watched.ticker
    }).then(({ data }) => data);
  }

  return Promise.reject();
};
