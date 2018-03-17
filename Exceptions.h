#pragma once

#include <exception>
#include <sstream>


class WindowException : public std::exception
{
public:
    WindowException(std::string error)
        : m_error(error) {}
    ~WindowException() throw() {}
    virtual const char* what() const throw()
    {
        return m_error.c_str();
    }
private:
    std::string m_error;
};

class ImageException : public std::exception
{
public:
    ImageException(std::string error)
        : m_error(error) {}
    ~ImageException() throw() {}
    virtual const char* what() const throw()
    {
        return m_error.c_str();
    }
private:
    std::string m_error;
};