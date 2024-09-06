import { Box, Typography, Avatar, Badge } from "@mui/material";


interface CardHeaderProps {
    teams: string;
    percentage: number;
    sportbook1: string;
    sportbook1_alias: string;
    sportbook2: string;
    sportbook2_alias: string;
    datetime: string;
}


const CardHeader: React.FC<CardHeaderProps> = ({ teams, percentage, sportbook1, sportbook2, sportbook1_alias, sportbook2_alias, datetime }) => {
    return (
        <Box>
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                sx={{ paddingBottom: '8px' }}
            >
                <Typography variant="subtitle1" sx={{ fontSize: '15.5px', fontWeight: 700, marginLeft: "8px", textAlign: "left", paddingTop: "2px" }}>
                    MONEYLINE
                </Typography>
                <Box display="flex" alignItems="center">
                    <Avatar src={sportbook1} alt={sportbook1_alias} sx={{ width: 24, height: 24, marginRight: '4px', borderRadius: '8px' }} />
                    <Avatar src={sportbook2} alt={sportbook2_alias} sx={{ width: 24, height: 24, marginRight: '69px', borderRadius: '8px' }} />
                    <Badge
                        color="success"
                        badgeContent={`${percentage}%`}
                        sx={{
                            "& .MuiBadge-badge": {
                                backgroundColor: "#4caf50",
                                color: "#fff",
                                fontSize: "14px",
                                padding: "13px 8px",
                                borderRadius: "8px",
                                marginRight: "34px",
                            },
                        }}
                    />
                </Box>
            </Box>

            {/* Date and Horizontal Line */}
            <Box display="flex" alignItems="center" sx={{ marginLeft: '8px', marginRight: '8px' }}>
                <Typography sx={{ fontSize: '13.5px', fontWeight: 700, textAlign: "left", marginRight: "8px" }}>
                    {datetime}
                </Typography>
                {/* Horizontal line */}
                <Box sx={{ flex: 1, height: '1px', backgroundColor: '#ccc' }} />
            </Box>


            <Box sx={{ height: '10px' }} />

            {/* Teams Info */}
            <Typography variant="h6" sx={{ fontSize: '16px', fontWeight: 600, textAlign: "left", marginLeft: "8px", lineHeight: "1.15" }}>
                {teams}
            </Typography>
            <Box sx={{ height: '5px' }} />

        </Box>
    );
};

export default CardHeader;
