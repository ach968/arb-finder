import { Box, Typography, Button, Avatar, Tooltip } from "@mui/material";

interface LineProps {
    line1: string;
    price1: string;
    point1: number;
    line2: string;
    price2: string;
    point2: number;
}

interface SportbookProp {
    picture: string;
    alias: string;
}

interface CardBodyProps {
    lineProps: LineProps;
    sportbooks: SportbookProp[];
}

const CardBody: React.FC<CardBodyProps> = ({ lineProps, sportbooks }) => {
    return (
        <Box display="flex" flexDirection="column" justifyContent="space-between" padding={"6px"}>
            <Box sx={{ height: '1px', margin: '4px 0' }} />

            <Box display="flex" alignItems="center">
                <Tooltip
                    title={sportbooks[0].alias}
                    placement="right"
                    arrow
                >
                    <Avatar src={sportbooks[0].picture} alt={sportbooks[0].alias}
                        sx={{
                            width: 32,
                            height: 32,
                            marginRight: '10px',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            transition: 'transform 0.3s ease',
                            '&:hover': {
                                transform: 'scale(1.2)',
                            }
                        }} />

                </Tooltip>
                <Typography variant="body1"
                    sx={{ textAlign: "left", flex: "1", fontWeight: 600, fontSize: "14px", marginRight: "8px" }}
                >{lineProps.line1} {lineProps.point1 > 0 ? "+" : ""}{lineProps.point1}
                </Typography>
                <Button variant="contained" disabled sx={{
                    fontSize: "15px",
                    padding: "3px 8px",
                    borderRadius: "13px",
                    "&.Mui-disabled": {
                        backgroundColor: 'gray',
                        color: 'white',
                        fontWeight: 600,
                    },
                }}>{lineProps.price1}</Button>
            </Box>
            <Box sx={{ height: '1px', margin: '4px 0' }} />
            <Box display="flex" alignItems="center">
                
                    <Avatar src={sportbooks[1].picture} alt={sportbooks[1].alias}
                        sx={{
                            width: 32,
                            height: 32,
                            marginRight: '10px',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            transition: 'transform 0.3s ease',
                            '&:hover': {
                                transform: 'scale(1.2)',
                            }
                        }} />
                <Typography variant="body1"
                    sx={{ textAlign: "left", flex: "1", fontWeight: 600, fontSize: "14px", marginRight: "8px" }}
                >{lineProps.line2} {lineProps.point2 > 0 ? "+" : ""}{lineProps.point2}</Typography>

                <Button variant="contained" disabled sx={{
                    fontSize: "15px",
                    padding: "3px 8px",
                    borderRadius: "13px",
                    "&.Mui-disabled": {
                        backgroundColor: 'gray',
                        color: 'white',
                        fontWeight: 600,
                    },
                }}>{lineProps.price2}</Button>
            </Box>
        </Box>
    );
};

export default CardBody;
