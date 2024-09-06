import { Card, CardContent } from "@mui/material";
import CardHeader from './CardHeader';
import CardBody from './CardBody';
import CardFooter from './CardFooter';

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
    };

    return (
        <Card sx={{ backgroundColor: '#333', color: '#fff', width: 300, borderRadius: 5 }}>
            <CardContent>
                <CardHeader teams={cardData.teams} percentage={cardData.percentage} />
                <CardBody overUnder={cardData.overUnder} />
                <CardFooter />
            </CardContent>
        </Card>
    );
};

export default CardComponent;
