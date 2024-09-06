import { Card, CardContent } from "@mui/material";
import CardHeader from './CardHeader';
import CardBody from './CardBody';
import CardFooter from './CardFooter';
import { createTheme, ThemeProvider } from "@mui/material/styles";

interface OverUnderProps {
    over: number;
    overOdds: string;
    under: number;
    underOdds: string;
}

interface CardDataProps {
    teams: string;
    percentage: number;
    overUnder: OverUnderProps;
    sportbook1: string;
    sportbook2: string;
    sportbook1_alias: string;
    sportbook2_alias: string;
}

const CardComponent: React.FC = () => {
    const cardData: CardDataProps = {
        teams: "Baltimore Ravens @ San Francisco 49ers",
        percentage: 3.93,
        overUnder: {
            over: 14.5,
            overOdds: "+145",
            under: 14.5,
            underOdds: "-130",
        },
        sportbook1: "https://yt3.googleusercontent.com/2iOdtiJYSw27WrYKkQc2uReDqQ3XhyUA1YSOus-Andxj6Rz6TfMI0jeFWWcwaJEzHU9kWKA4=s900-c-k-c0x00ffffff-no-rj",
        sportbook2: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHZG35WfrgOR2UkQPpRN4inxSnrypyJYNhYA&s",
        sportbook1_alias: "FanDuel",
        sportbook2_alias: "Fliff",
    };

    const theme = createTheme({
        typography: {
            fontFamily: 'Inter,sans-serif',
        }
    });

    return (
        <ThemeProvider theme={theme}>
            <Card sx={{ backgroundColor: '#333', color: '#fff', width: 300, borderRadius: 5 }}>
                <CardContent>
                    <CardHeader teams={cardData.teams} percentage={cardData.percentage}
                        sportbook1={cardData.sportbook1}
                        sportbook2={cardData.sportbook2}
                        sportbook1_alias={cardData.sportbook1_alias}
                        sportbook2_alias={cardData.sportbook2_alias} />
                    <CardBody overUnder={cardData.overUnder}
                        sportbook1={cardData.sportbook1}
                        sportbook2={cardData.sportbook2}
                        sportbook1_alias={cardData.sportbook1_alias}
                        sportbook2_alias={cardData.sportbook2_alias}
                    />
                    <CardFooter />
                </CardContent>
            </Card>
        </ThemeProvider>
    );
};

export default CardComponent;
