import { Card, CardContent } from "@mui/material";
import CardHeader from './CardHeader';
import CardBody from './CardBody';
import CardFooter from './CardFooter';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import BookmakerLogos from "../../assets/BookmakerLogos";

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
    commence_time: string;
}

interface SpreadsCardComponentProps {
    data: CardDataProps;
    onBetClick: () => void;
}

const SpreadsCardComponent: React.FC<SpreadsCardComponentProps> = ({ data, onBetClick }) => {
    const theme = createTheme({
        typography: {
            fontFamily: 'Inter,sans-serif',
        }
    });

    // Convert UNIX timestamp (in seconds) to a formatted EST date/time string
    const estDate = new Date(Number(data.commence_time) * 1000).toLocaleString('en-US', {
        timeZone: 'America/New_York',  // Ensure the time is in EST
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,  // 12-hour format
    }) + ' (EST)';

    // Map the data to the structure your component expects
    const cardData = {
        teams: data.game_title,
        percentage: data.expected_value * 100,  // Convert expected value to percentage
        lineProps: {
            line1: data.line_1.name,
            price1: `${data.line_1.price > 0 ? '+' : ''}${data.line_1.price}`,
            point1: data.line_1.point,
            line2: data.line_2.name,
            price2: `${data.line_2.price > 0 ? '+' : ''}${data.line_2.price}`,
            point2: data.line_2.point,
        },
        sportbook1: BookmakerLogos[data.line_1.bookmaker as keyof typeof BookmakerLogos],  // Get logo URL for sportbook1
        sportbook2: BookmakerLogos[data.line_2.bookmaker as keyof typeof BookmakerLogos],  // Get logo URL for sportbook2
        sportbook1_alias: data.line_1.bookmaker,
        sportbook2_alias: data.line_2.bookmaker,
        commence_time: estDate  // Use formatted EST date/time
    };

    return (
        <ThemeProvider theme={theme}>
            <Card sx={{ backgroundColor: '#333', color: '#fff', width: 325, borderRadius: 5 }}>
                <CardContent>
                    {/* Header with teams, percentage and formatted EST datetime */}
                    <CardHeader
                        teams={cardData.teams}
                        percentage={cardData.percentage.toPrecision(3)}
                        sportbook1={cardData.sportbook1}   // Pass logo URL for sportbook1
                        sportbook2={cardData.sportbook2}   // Pass logo URL for sportbook2
                        sportbook1_alias={cardData.sportbook1_alias}
                        sportbook2_alias={cardData.sportbook2_alias}
                        datetime={cardData.commence_time}  // Display formatted EST date/time
                    />
                    {/* Body with team names, prices, and points */}
                    <CardBody
                        lineProps={cardData.lineProps}
                        sportbooks={[
                            { picture: cardData.sportbook1, alias: cardData.sportbook1_alias },
                            { picture: cardData.sportbook2, alias: cardData.sportbook2_alias }
                        ]}
                    />
                    {/* Footer */}
                    <CardFooter onBetClick={onBetClick}/>
                </CardContent>
            </Card>
        </ThemeProvider>
    );
};

export default SpreadsCardComponent;
