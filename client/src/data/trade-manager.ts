import Trade from "./models/trade";
import axios from "axios";

class TradeManager {
  async allTrades(): Promise<Trade[]> {
    console.log("Hello");
    return axios.get("/trades").then(res => {
      console.log(res);
      return [];
    });
  }
}

export default TradeManager;
