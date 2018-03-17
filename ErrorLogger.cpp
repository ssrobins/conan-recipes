#include <fstream>
#include <string>
#include "ErrorLogger.h"
#include "Exceptions.h"

ErrorLogger::ErrorLogger(std::string const& logFileName) : m_logFileName(logFileName)
{
    // Remove the file so we don't see errors from a previous run of the program
    std::remove(m_logFileName.c_str());
}

ErrorLogger::~ErrorLogger()
{

}

std::ofstream ErrorLogger::operator<<(std::string const& error)
{
    std::ofstream outputFileStream;

    // Open the file now instead of in the constructor so an error log file is only created
    // when there is an error to report.
    // Append to the file, in case there are multiple error messages in the same session.
    outputFileStream.open(m_logFileName.c_str(), std::ofstream::app);

    outputFileStream << error;
    return outputFileStream;
}
