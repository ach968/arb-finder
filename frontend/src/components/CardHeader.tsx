import { Box, Typography, Avatar, Badge } from "@mui/material";

interface CardHeaderProps {
    teams: string;
    percentage: number;
}

const CardHeader: React.FC<CardHeaderProps> = ({ teams, percentage }) => {
    return (
        <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">{teams}</Typography>
            <Box display="flex" alignItems="center">
                <Avatar src="/path-to-fanduel-logo.png" alt="FanDuel" />
                <Avatar src="/path-to-logo.png" alt="Other Book" />
                <Badge
                    color="success"
                    badgeContent={`${percentage}%`}
                    anchorOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                    }}
                />
            </Box>
        </Box>
    );
};

export default CardHeader;
