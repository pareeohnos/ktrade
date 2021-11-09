interface Trade {
  id: number;
  ticker: string;
  orderId: number;
  orderStatus: String;
  orderStatusDesc: String;
  currentPositionSize: number;
  filled: number;
  priceAtOrder: number;
  orderedAt: Date;
}

class Trade {}

export default Trade;
