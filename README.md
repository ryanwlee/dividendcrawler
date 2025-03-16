# YieldMax ETF Explorer

A modern web application built with Next.js that allows users to explore and analyze YieldMax ETF distributions and their relationship with underlying stock prices.

![YieldMax ETF Explorer](preview.png)

## Features

- 🔍 **Interactive ETF Search**: Easily search and select from available YieldMax ETFs using a modern searchable dropdown
- 📊 **Dual-Axis Chart Visualization**:
  - View distribution history alongside underlying stock prices
  - Interactive tooltips showing precise values
  - Color-coded data series for clear differentiation
- 🎨 **Modern Dark Theme**: Sleek dark mode interface with carefully chosen color palette
- 📱 **Responsive Design**: Fully responsive layout that works on desktop and mobile devices
- 📈 **Detailed ETF Information**:
  - Display of ETF symbol and full name
  - Distribution count tracking
  - Clear presentation of historical data

## Tech Stack

- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with React-Chartjs-2
- **Data**: JSON-based data store

## Getting Started

### Prerequisites

- Node.js 18.0 or later
- npm or yarn package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dividendcrawler.git
cd dividendcrawler
```

2. Install dependencies:

```bash
cd frontend
npm install
# or
yarn install
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── page.tsx          # Main application page
│   │   └── components/
│   │   └── data/
│   └── public/
│       └── ...                   # Static assets
```

## Data Structure

The application uses two main JSON files for data:

1. `yieldmax_etf_successful.json`:

   - List of all available ETFs
   - Basic metadata (symbol, name, distribution count)

2. `yieldmax_etf_distribution.json`:
   - Detailed distribution history for each ETF
   - Underlying stock price data
   - Dates and amounts for each distribution

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- YieldMax ETFs for providing the underlying investment products
- The Next.js team for the excellent framework
- The Chart.js team for the powerful charting library
