import { Box, Typography, Button, Avatar } from "@mui/material";

interface OverUnderProps {
    over: number;
    overOdds: string;
    under: number;
    underOdds: string;
}

interface CardBodyProps {
    overUnder: OverUnderProps;
}

const CardBody: React.FC<CardBodyProps> = ({ overUnder }) => {
    return (
        <Box display="flex" flexDirection="column" justifyContent="space-between" padding={2}>
            <Box display="flex" alignItems="center">
                <Avatar src="/path-to-fanduel-logo.png" alt="FanDuel" />
                <Typography variant="body1">O{overUnder.over}</Typography>
                <Button variant="contained" disabled>{overUnder.overOdds}</Button>
            </Box>
            <Box display="flex" alignItems="center">
                <Avatar src="/path-to-logo.png" alt="Other Book" />
                <Typography variant="body1">U{overUnder.under}</Typography>
                <Button variant="contained" disabled>{overUnder.underOdds}</Button>
            </Box>
        </Box>
    );
};

export default CardBody;
