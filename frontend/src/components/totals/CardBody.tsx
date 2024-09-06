import { Box, Typography, Button, Avatar } from "@mui/material";

interface OverUnderProps {
    over: number;
    overOdds: string;
    under: number;
    underOdds: string;
}

interface CardBodyProps {
    overUnder: OverUnderProps;
    sportbook1: string;
    sportbook1_alias: string;
    sportbook2: string;
    sportbook2_alias: string;
}

const CardBody: React.FC<CardBodyProps> = ({ overUnder, sportbook1, sportbook2, sportbook1_alias, sportbook2_alias }) => {
    return (
        <Box display="flex" flexDirection="column" justifyContent="space-between" padding={"6px"}>
            <Box sx={{ height: '1px', margin: '4px 0' }} />

            <Box display="flex" alignItems="center">
                <Avatar src={sportbook1} alt={sportbook1_alias} sx={{ width: 24, height: 24, marginRight: '10px', borderRadius: '8px' }} />
                <Typography variant="body1"
                    sx={{ textAlign: "center", flex: "1", fontWeight: 600, fontSize: "16px" }}
                >{overUnder.over}</Typography>
                <Button variant="contained" disabled sx={{
                    fontSize: "15px",
                    padding: "3px 8px",
                    borderRadius: "13px",
                    "&.Mui-disabled": {
                        backgroundColor: 'gray',
                        color: 'white',
                        fontWeight: 600,
                    },
                }}>{overUnder.overOdds}</Button>
            </Box>
            <Box sx={{ height: '1px', margin: '6px 0' }} />
            <Box display="flex" alignItems="center">
                <Avatar src={sportbook2} alt={sportbook2_alias} sx={{ width: 24, height: 24, marginRight: '10px', borderRadius: '8px' }} />
                <Typography variant="body1"
                    sx={{ textAlign: "center", flex: "1", fontWeight: 600, fontSize: "16px" }}
                >{overUnder.under}</Typography>

                <Button variant="contained" disabled sx={{
                    fontSize: "15px",
                    padding: "3px 8px",
                    borderRadius: "13px",
                    "&.Mui-disabled": {
                        backgroundColor: 'gray',
                        color: 'white',
                        fontWeight: 600,
                    },
                }}>{overUnder.underOdds}</Button>
            </Box>
        </Box>
    );
};

export default CardBody;
