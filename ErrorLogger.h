#pragma once

#include <string>
#include <fstream>

class ErrorLogger
{
public:
    ErrorLogger(std::string const&);
    ~ErrorLogger();

    std::ofstream operator<<(std::string const&);

private:
    std::string m_logFileName;
};