import { Box, Button, colors, Collapse, Typography } from "@mui/material";

interface CardFooterProps {
    onBetClick: () => void;  // Define the prop for handling the BET button click
}

const CardFooter: React.FC<CardFooterProps> = ({onBetClick}) => {

    return (
        <Box textAlign="center" padding={1}>
            {/* Main BET Button */}
            <Button variant="contained"
                disableRipple
                onClick={onBetClick}
                sx={{
                    backgroundColor: "#333",
                    color: colors.common.white,
                    padding: '10px 20px',
                    borderRadius: '8px',
                    borderColor: colors.grey[900],
                    outline: 'none',
                    borderWidth: '2px',
                    borderStyle: 'solid',
                    fontWeight: 600,
                    fontSize: '15px',
                    textTransform: 'capitalize',
                    '&:hover': {
                        backgroundColor: colors.green[700],
                        outline: 'none',
                    },
                    width: '100%',
                    marginTop: '15px',
                    marginBottom: '-10px',
                    '&:focus': {
                        outline: 'none',
                    },
                }}
            >
                {"BET"}
            </Button>

        </Box>
    );
};

export default CardFooter;
