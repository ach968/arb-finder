import React from 'react';
import { Box, Grid, Avatar, Typography, Button, Divider } from '@mui/material';
import BookmakerLogos from '../assets/BookmakerLogos';

interface BetOverviewProps {
    bookmaker1: string;
    bookmaker2: string;
    odds1: string;
    odds2: string;
    stake1: string;
    stake2: string;
    hit1: string;
    hit2: string;
    payout1: string;
    payout2: string;
    returnPercentage: string;
}

const BetOverview: React.FC<BetOverviewProps> = ({
    bookmaker1,
    bookmaker2,
    odds1,
    odds2,
    stake1,
    stake2,
    hit1,
    hit2,
    payout1,
    payout2,
    returnPercentage,
}) => {
    return (
        <Box
            sx={{
                backgroundColor: '#333',
                borderRadius: '12px',
                padding: '20px',
                maxWidth: '800px',  // Make it wider for the two columns
                color: 'white',
                textAlign: 'center',
                margin: '0 auto'  // Center the modal
            }}
        >
            <Typography variant="h6" sx={{ marginBottom: '20px' }}>
                BET OVERVIEW - MONEYLINE
            </Typography>

            <Grid container spacing={2} justifyContent="space-between" alignItems="center">
                {/* First Column */}
                <Grid item xs={5}>
                    <Typography variant="h4">1</Typography>
                    <Avatar
                        src={BookmakerLogos[bookmaker1 as keyof typeof BookmakerLogos]}
                        alt={bookmaker1}
                        sx={{ width: 50, height: 50, marginBottom: '10px', borderRadius: '18px', alignItems: 'center' }}
                    />
                    <Typography variant="h6">{bookmaker1}</Typography>
                    <Button
                        variant="contained"
                        disabled
                        sx={{ margin: '10px 0', backgroundColor: 'gray', color: 'white', borderRadius: '20px' }}
                    >
                        {odds1}
                    </Button>
                    <Typography>% HIT</Typography>
                    <Button variant="contained" disabled sx={{ margin: '5px 0', backgroundColor: 'gray', color: 'white' }}>
                        {hit1}
                    </Button>
                    <Typography>Stake</Typography>
                    <Button variant="contained" disabled sx={{ margin: '5px 0', backgroundColor: 'gray', color: 'white' }}>
                        {stake1}
                    </Button>
                    <Typography>Expected Payout</Typography>
                    <Typography variant="h5" sx={{ fontWeight: 'bold', marginTop: '5px' }}>
                        {payout1}%
                    </Typography>
                </Grid>

                {/* Divider */}
                <Grid item xs={1}>
                    <Divider orientation="vertical" sx={{ backgroundColor: 'gray', height: '100%' }} />
                </Grid>

                {/* Second Column */}
                <Grid item xs={5}>
                    <Typography variant="h4">2</Typography>
                    <Avatar
                        src={BookmakerLogos[bookmaker2 as keyof typeof BookmakerLogos]}
                        alt={bookmaker2}
                        sx={{ width: 50, height: 50, marginBottom: '10px' }}
                    />
                    <Typography variant="h6">{bookmaker2}</Typography>
                    <Button
                        variant="contained"
                        disabled
                        sx={{ margin: '10px 0', backgroundColor: 'gray', color: 'white', borderRadius: '20px' }}
                    >
                        {odds2}
                    </Button>
                    <Typography>% HIT</Typography>
                    <Button variant="contained" disabled sx={{ margin: '5px 0', backgroundColor: 'gray', color: 'white' }}>
                        {hit2}
                    </Button>
                    <Typography>Stake</Typography>
                    <Button variant="contained" disabled sx={{ margin: '5px 0', backgroundColor: 'gray', color: 'white' }}>
                        {stake2}
                    </Button>
                    <Typography>Expected Payout</Typography>
                    <Typography variant="h5" sx={{ fontWeight: 'bold', marginTop: '5px' }}>
                        {payout2}%
                    </Typography>
                </Grid>
            </Grid>

            {/* Return Section */}
            <Divider sx={{ margin: '20px 0', backgroundColor: 'gray' }} />
            <Typography variant="h6" sx={{ marginBottom: '10px' }}>
                Return
            </Typography>
            <Button
                variant="contained"
                sx={{ backgroundColor: '#4caf50', color: 'white', fontWeight: 'bold', fontSize: '18px', borderRadius: '20px' }}
            >
                {returnPercentage}
            </Button>
        </Box>
    );
};

export default BetOverview;
