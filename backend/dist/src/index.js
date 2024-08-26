import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import fetchArbData from "./routes/fetchArbData.js";
import pullArbData from "./routes/pullArbData.js";
const app = express();
const PORT = process.env.PORT || 5001;
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
/**
 * Fetch arb opportunities route
 */
app.use("/api/fetch_arb_data", fetchArbData);
/**
 * Pull arb opportunities route
 */
app.use("/api/pull_arb_data", pullArbData);
/**
 * Default route
 */
app.get("/", (_req, _res) => { });
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
