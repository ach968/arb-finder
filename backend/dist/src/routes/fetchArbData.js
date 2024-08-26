import express from "express";
import axios from "axios";
const router = express.Router();
router.get("/", async (_req, res) => {
    try {
        const response = await axios.get("http://localhost:5000/api/arb_opportunity?get_latest_data=true");
        res.status(response.status).json(response.data);
    }
    catch (error) {
        res.status(error.response ? error.response.status : 500).json({
            error: error.message,
        });
    }
});
export default router;
