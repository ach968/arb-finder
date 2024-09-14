import React from 'react';
import { Box, Grid, Avatar, Typography, Button, Divider, colors } from '@mui/material';
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
                width: '650px',
                borderRadius: '1px',
                padding: '20px',
                color: 'white',
                textAlign: 'center',
                margin: '0 auto'  // Center the modal
            }}
        >
            <Typography variant="h5" fontWeight={600} sx={{ marginBottom: '10px' }}>
                BET OVERVIEW
            </Typography>

            <Grid container spacing={2} justifyContent="space-between" alignItems="stretch">
                {/* First Column */}
                <Grid item xs={5} textAlign="center">
                    <Typography variant="h4" fontWeight={600} marginBottom={2}>1</Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                        <Avatar
                            src={BookmakerLogos[bookmaker1 as keyof typeof BookmakerLogos]}
                            alt={bookmaker1}
                            sx={{ width: 50, height: 50, marginBottom: '10px', borderRadius: '10px' }}
                        />
                    </Box>
                    <Typography variant="h6">{bookmaker1}</Typography>
                    <Button
                        variant="outlined"
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
                <Grid item xs={1} sx={{ display: "flex", justifyContent: 'center' }}>
                    <Divider orientation="vertical" sx={{ backgroundColor: 'gray', height: '100%' }} />
                </Grid>

                {/* Second Column (Replicated from the First Column) */}
                <Grid item xs={5} textAlign="center">
                    <Typography variant="h4" fontWeight={600} marginBottom={2}>2</Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                        <Avatar
                            src={BookmakerLogos[bookmaker2 as keyof typeof BookmakerLogos]}
                            alt={bookmaker2}
                            sx={{ width: 50, height: 50, marginBottom: '10px', borderRadius: '10px' }}
                        />
                    </Box>
                    <Typography variant="h6">{bookmaker2}</Typography>
                    <Box
                        sx={{ margin: '10px auto', backgroundColor: 'gray', color: 'white !important', borderRadius: '20px', fontWeight: 600 , maxWidth: '65px',padding: '8px' }}
                    >
                        {Number(odds2) > 0 ? `${'+' + odds2}` : odds2}
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <Typography sx={{ fontWeight: 600 }}>implied prob</Typography>
                        <Box
                            sx={{
                                margin: '5px 0',
                                backgroundColor: colors.grey[800],
                                color: 'white',
                                padding: '8px 16px',
                                borderRadius: '4px',
                                marginLeft: '20px',
                                border: '1px solid',  // Mimic button's appearance
                                borderColor: colors.grey[700],  // Border for outlined style
                            }}
                        >
                            {/* Span with selectable text */}
                            <span>{hit2}</span>
                        </Box>
                    </Box>
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

            <Typography variant="h6" sx={{ marginBottom: '10px', marginTop: '20px' }}>
                Return
            </Typography>
            <Button
                disabled
                variant="outlined"
                sx={{ backgroundColor: '#4caf50', color: 'white', fontWeight: 'bold', fontSize: '18px', borderRadius: '20px' }}
            >
                {returnPercentage}
            </Button>
        </Box>
    );
};

export default BetOverview;
