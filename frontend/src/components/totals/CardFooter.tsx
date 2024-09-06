import { Box, Button, colors } from "@mui/material";

const CardFooter: React.FC = () => {
    return (
        <Box textAlign="center" padding={1}>
            <Button variant="contained"
                sx={{
                    backgroundColor: "#333",
                    color: colors.common.white,
                    padding: '10px 20px',
                    borderRadius: '11px',
                    borderColor: colors.grey[900],
                    borderWidth: '2px',
                    borderStyle: 'solid',
                    fontWeight: 600,
                    fontSize: '15px',
                    textTransform: 'capitalize',
                    '&:hover': {
                        backgroundColor: colors.green[700],
                    },
                    width: '100%',
                    marginTop: '15px',
                    marginBottom: '-10px'

                }}

            >TAKE BET</Button>
        </Box >
    );
};

export default CardFooter;
