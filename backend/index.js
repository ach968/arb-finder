import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import fetchArbOpportunities from "./routes/fetchArbOpportunities.js";
import pullArbOpportunities from "./routes/pullArbOpportunities.js";

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

/**
 * Fetch arb opportunities route
 */
app.use("/api/fetch_arb_data", fetchArbOpportunities);

/**
 * Pull arb opportunities route
 */
app.use("/api/pull_arb_data", pullArbOpportunities);

/**
 * Default route
 */
app.get("/", (req, res) => {});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
