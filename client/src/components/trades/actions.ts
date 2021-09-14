import Trade from "@/data/models/trade";
import axios from "axios";

export const trim = (trade: Trade, amount: String): Promise<Trade> => {
  return axios.post("/trim", {
    trade: trade.id,
    amount: amount
  }).then(({ data }) => data);
};