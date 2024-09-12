import { Card, CardContent } from "@mui/material";
import CardHeader from './CardHeader';
import CardBody from './CardBody';
import CardFooter from './CardFooter';  // Ensure CardFooter has the onBetClick functionality
import { createTheme, ThemeProvider } from "@mui/material/styles";

interface LineProps {
    bookmaker: string;
    name: string;
    point: number;
    price: number;
}

interface CardDataProps {
    game_title: string;
    expected_value: number;
    line_1: LineProps;
    line_2: LineProps;
}

interface H2HCardComponentProps {
    data: CardDataProps;
    onBetClick: () => void;
}

const H2HCardComponent: React.FC<H2HCardComponentProps> = ({ data, onBetClick }) => {
    const theme = createTheme({
        typography: {
            fontFamily: 'Inter,sans-serif',
        }
    });

    // Map the data to the structure your component expects
    const cardData = {
        teams: data.game_title,
        percentage: data.expected_value * 100,  // Convert expected value to percentage
        lineProps: {
            team1: data.line_1.name,
            price1: `${data.line_1.price > 0 ? '+' : ''}${data.line_1.price}`,  // Add "+" to positive prices
            team2: data.line_2.name,
            price2: `${data.line_2.price > 0 ? '+' : ''}${data.line_2.price}`,
        },
        sportbook1: data.line_1.bookmaker,
        sportbook2: data.line_2.bookmaker,
        sportbook1_alias: data.line_1.bookmaker,
        sportbook2_alias: data.line_2.bookmaker,
    };

    return (
        <ThemeProvider theme={theme}>
            <Card sx={{ backgroundColor: '#333', color: '#fff', width: 325, borderRadius: 5 }}>
                <CardContent>
                    <CardHeader
                        teams={cardData.teams}
                        percentage={cardData.percentage}
                        sportbook1={cardData.sportbook1}
                        sportbook2={cardData.sportbook2}
                        sportbook1_alias={cardData.sportbook1_alias}
                        sportbook2_alias={cardData.sportbook2_alias}
                        datetime="Today 8:20 PM"  // You can update this dynamically if needed
                    />
                    <CardBody
                        lineProps={cardData.lineProps}
                        sportbooks={[
                            { picture: cardData.sportbook1, alias: cardData.sportbook1_alias },
                            { picture: cardData.sportbook2, alias: cardData.sportbook2_alias }
                        ]}
                    />
                    {/* Pass onBetClick to CardFooter */}
                    <CardFooter onBetClick={onBetClick} />
                </CardContent>
            </Card>
        </ThemeProvider>
    );
};

export default H2HCardComponent;
