#include <iostream>
#include <string>
#include <filesystem>
#include <fstream>

using namespace std;
namespace fs = filesystem;

//finding a pair and display it historical data
void find_symbol(string symbol){
    //full path to file
    fs::path folder = "C:/Users/Student/.vscode/Projects-2025/markets-analysis/historical_data";
    fs::path filename = symbol + "_history.txt";
    fs::path filepath = folder / filename;

    if (!fs::exists(filepath)) {
        cerr << "File not found: " << filepath << "\n";
        return;
    }

    //reading file
    ifstream infile(filepath);
    string line;
    while (getline(infile, line)) {
        cout << line << endl;  
    }

}

int main() {
    cout << "Welcome, Let's do some analysis...!" << endl;
    cout << endl;

    string ticker;
    cout << "Enter symbol(e.g USDZAR=X or NVDA): ";
    cin >> ticker;

    find_symbol(ticker);

    return 0;
}
#include <iostream>
#include <string>
#include <filesystem>
#include <fstream>

using namespace std;
namespace fs = filesystem;

//finding a pair and display it historical data
void find_symbol(string symbol){
    //full path to file
    fs::path folder = "C:/Users/Student/.vscode/Projects-2025/markets-analysis/historical_data";
    fs::path filename = symbol + "_history.txt";
    fs::path filepath = folder / filename;

    if (!fs::exists(filepath)) {
        cerr << "File not found: " << filepath << "\n";
        return;
    }

    //reading file
    ifstream infile(filepath);
    string line;
    while (getline(infile, line)) {
        cout << line << endl;  
    }

}

int main() {
    cout << "Welcome, Let's do some analysis...!" << endl;
    cout << endl;

    string ticker;
    cout << "Enter symbol(e.g USDZAR=X or NVDA): ";
    cin >> ticker;

    find_symbol(ticker);

    return 0;
}
