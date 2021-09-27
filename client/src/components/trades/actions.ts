import Trade from "@/data/models/trade";
import axios, { AxiosError } from "axios";
// @ts-ignore
import { notify } from "notiwind";

const errHandler = (err: Error | AxiosError) => {
  if (axios.isAxiosError(err)) {
    if (err.response?.data?.error) {
      alert(err.response?.data.error);
    } else {
      alert("Unexpected error occurred");
    }
  } else {
    alert("Unexpected error occurred");
  }
  throw err;
};

export const closePosition = (trade: Trade): Promise<void> => {
  return axios
    .post(`/trades/${trade.id}/close`)
    .then(() => {
      notify({
        group: "notifications",
        title: "Placed SELL order",
        text: "A SELL order was placed to close this position",
      });
    })
    .catch(errHandler);
};

/**
 * Deletes the specified trade from the system. Deleting a trade
 * will not close a position, it will simply be removed from the
 * database
 *
 * @param trade
 * @returns
 */
export const deleteTrade = (trade: Trade): Promise<void> => {
  return axios
    .delete(`/trades/${trade.id}`)
    .then(() => {
      notify({
        group: "notifications",
        title: "Deleted",
        text: "The trade was successfully deleted",
      });
    })
    .catch(errHandler);
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
  return axios
    .post("/trim", {
      trade: trade.id,
      amount: amount,
    })
    .then(({ data }) => data)
    .then(() => {
      notify(
        {
          group: "notifications",
          title: "Pending",
          text: `Requested sell of 1/3 of ${trade.ticker}`,
        },
        2000
      );
    })
    .catch(errHandler);
};
