import Trade from "./models/trade";
import axios from "axios";

class TradeManager {
  async allTrades(): Promise<Trade[]> {
    return axios.get("/trades").then(res => {
      return [];
    });
  }
}

export default TradeManager;
