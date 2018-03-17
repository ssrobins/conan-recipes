#pragma once

#include <string>
#include <fstream>

class ErrorHandler
{
public:
    ErrorHandler(std::string const&);
    ~ErrorHandler();

    std::ofstream operator<<(std::string const&);

private:
    std::string m_logFileName;
};