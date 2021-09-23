import Trade from "@/data/models/trade";
import axios from "axios";
// @ts-ignore
import { notify } from "notiwind";

export const deleteTrade = (trade: Trade): Promise<void> => {
  return axios.delete(`/trades/${trade.id}`)
    .then(() => {
      notify({
        group: "notifications",
        title: "Deleted",
        text: "The trade was successfully deleted"
      });
    })
    .catch(err => {
      if (err.response?.data?.error) {
        alert(err.response?.data.error);
      } else {
        alert("Unexpected error occurred");
      }
      throw err;
    })
};

/**
 * Trims the given trade by the given amount. Valid amounts are
 * 
 * THIRD
 * HALF
 * 
 * @param trade 
 * @param amount 
 * @returns 
 */
export const trimPosition = (trade: Trade, amount: String): Promise<void> => {
  return axios.post("/trim", {
    trade: trade.id,
    amount: amount
  }).then(({ data }) => data).then(() => {
    notify({
      group: "notifications",
      title: "Pending",
      text: `Requested sell of 1/3 of ${trade.ticker}`
    }, 2000);
  }).catch(err => {
    if (err.response?.data?.error) {
      alert(err.response?.data.error);
    } else {
      alert("Unexpected error occurred");
    }
  });;
};