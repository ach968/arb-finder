import express from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();
const router = express.Router();

// @ts-ignore
const l1 = [
  "soccer_epl",
  "soccer_france_ligue_one",
  "soccer_germany_bundesliga",
  "soccer_italy_serie_a",
  "soccer_mexico_ligamx",
  "soccer_spain_la_liga",
  "soccer_turkey_super_league",
  "soccer_uefa_champs_league_qualification",
  "soccer_uefa_europa_conference_league",
  "soccer_uefa_europa_league",
  "soccer_usa_mls",
  "americanfootball_nfl",
  "americanfootball_cfl",
  "baseball_mlb",
  "basketball_nba",
  "basketball_wnba",
  "icehockey_nhl",
  "mma_mixed_martial_arts",
];
// @ts-ignore
const l2 = [
  "americanfootball_cfl",
  "americanfootball_ncaaf",
  "americanfootball_ncaaf_championship_winner",
  "americanfootball_nfl",
  "americanfootball_nfl_preseason",
  "americanfootball_nfl_super_bowl_winner",
  "aussierules_afl",
  "baseball_kbo",
  "baseball_mlb",
  "baseball_mlb_world_series_winner",
  "baseball_npb",
  "basketball_nba",
  "basketball_nba_championship_winner",
  "basketball_ncaab_championship_winner",
  "basketball_wnba",
  "boxing_boxing",
  "cricket_t20_blast",
  "cricket_test_match",
  "cricket_the_hundred",
  "golf_masters_tournament_winner",
  "golf_pga_championship_winner",
  "icehockey_nhl",
  "icehockey_nhl_championship_winner",
  "icehockey_sweden_hockey_league",
  "lacrosse_pll",
  "mma_mixed_martial_arts",
  "politics_us_presidential_election_winner",
  "rugbyleague_nrl",
  "soccer_argentina_primera_division",
  "soccer_austria_bundesliga",
  "soccer_belgium_first_div",
  "soccer_brazil_campeonato",
  "soccer_brazil_serie_b",
  "soccer_chile_campeonato",
  "soccer_conmebol_copa_libertadores",
  "soccer_denmark_superliga",
  "soccer_efl_champ",
  "soccer_england_efl_cup",
  "soccer_england_league1",
  "soccer_england_league2",
  "soccer_epl",
  "soccer_fifa_world_cup_winner",
  "soccer_finland_veikkausliiga",
  "soccer_france_ligue_one",
  "soccer_france_ligue_two",
  "soccer_germany_bundesliga",
  "soccer_germany_bundesliga2",
  "soccer_germany_liga3",
  "soccer_greece_super_league",
  "soccer_italy_serie_a",
  "soccer_italy_serie_b",
  "soccer_japan_j_league",
  "soccer_korea_kleague1",
  "soccer_league_of_ireland",
  "soccer_mexico_ligamx",
  "soccer_netherlands_eredivisie",
  "soccer_norway_eliteserien",
  "soccer_poland_ekstraklasa",
  "soccer_portugal_primeira_liga",
  "soccer_spain_la_liga",
  "soccer_spain_segunda_division",
  "soccer_spl",
  "soccer_sweden_allsvenskan",
  "soccer_sweden_superettan",
  "soccer_switzerland_superleague",
  "soccer_turkey_super_league",
  "soccer_uefa_champs_league_qualification",
  "soccer_uefa_europa_conference_league",
  "soccer_uefa_europa_league",
  "soccer_usa_mls",
  "tennis_atp_cincinnati_open",
  "tennis_wta_cincinnati_open",
];
// @ts-ignore
const l3 = [
  "soccer_epl",
  "basketball_nba",
  "americanfootball_nfl",
]

router.get("/", async (_req, res) => {
  try {
    const requestBody = {
      sports: l2,
      markets: ["h2h","spreads","totals"],
      time_sent: Date.now() / 1000, // Current time in seconds
      bookmakers: [""],
      regions: ["us","us2"],
    };

    const response = await axios.post(
      "http://localhost:5000/api/arb_opportunity",
      requestBody,
      {
        headers: {
          "x-api-key": "a06923bffa794007036e956d4a22e3cb",
          "Content-Type": "application/json",
        },
      }
    );
    res.status(response.status).json(response.data);
  } catch (error: any) {
    res.status(error.response ? error.response.status : 500).json({
      error: error.message,
    });
  }
});

export default router;
