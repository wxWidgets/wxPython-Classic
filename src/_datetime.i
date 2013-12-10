/////////////////////////////////////////////////////////////////////////////
// Name:        _datetime.i
// Purpose:     SWIG interface for wxDateTime and etc.
//
// Author:      Robin Dunn
//
// Created:     25-Nov-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

%{
#include <wx/datetime.h>
%}

MAKE_CONST_WXSTRING(DefaultDateTimeFormat);
MAKE_CONST_WXSTRING(DefaultTimeSpanFormat);

//---------------------------------------------------------------------------


%typemap(in) wxDateTime::TimeZone& (bool temp=false) {
    $1 = new wxDateTime::TimeZone((wxDateTime::TZ)PyInt_AsLong($input));
    temp = true;
}
%typemap(freearg) wxDateTime::TimeZone& {
    if (temp$argnum) delete $1;
}


%{
#define LOCAL_TZ wxDateTime::Local
%}


// Convert a wxLongLong to a Python Long by getting the hi/lo dwords, then
// shifting and oring them together
%typemap(out) wxLongLong {
    #if wxUSE_LONGLONG_NATIVE
        return PyLong_FromLongLong(sipCpp->GetValue());
    #else
        PyObject *hi, *lo, *shifter, *shifted;
        hi = PyLong_FromLong( $1.GetHi() );
        lo = PyLong_FromLong( $1.GetLo() );
        shifter = PyLong_FromLong(32);
        shifted = PyNumber_Lshift(hi, shifter);
        $result = PyNumber_Or(shifted, lo);
        Py_DECREF(hi);
        Py_DECREF(lo);
        Py_DECREF(shifter);
        Py_DECREF(shifted);
    #endif
}


//---------------------------------------------------------------------------

//typedef unsigned short wxDateTime_t;
#define wxDateTime_t int

// wxDateTime represents an absolute moment in the time
class wxDateTime {
public:

    enum TZ
    {
        // the time in the current time zone
        Local,

        // zones from GMT (= Greenwhich Mean Time): they're guaranteed to be
        // consequent numbers, so writing something like `GMT0 + offset' is
        // safe if abs(offset) <= 12
        // underscore stands for minus
        GMT_12, GMT_11, GMT_10, GMT_9, GMT_8, GMT_7,
        GMT_6, GMT_5, GMT_4, GMT_3, GMT_2, GMT_1,
        GMT0,
        GMT1, GMT2, GMT3, GMT4, GMT5, GMT6,
        GMT7, GMT8, GMT9, GMT10, GMT11, GMT12, GMT13,

        // Europe
        WET = GMT0,                         // Western Europe Time
        WEST = GMT1,                        // Western Europe Summer Time
        CET = GMT1,                         // Central Europe Time
        CEST = GMT2,                        // Central Europe Summer Time
        EET = GMT2,                         // Eastern Europe Time
        EEST = GMT3,                        // Eastern Europe Summer Time
        MSK = GMT3,                         // Moscow Time
        MSD = GMT4,                         // Moscow Summer Time

        // US and Canada
        AST = GMT_4,                        // Atlantic Standard Time
        ADT = GMT_3,                        // Atlantic Daylight Time
        EST = GMT_5,                        // Eastern Standard Time
        EDT = GMT_4,                        // Eastern Daylight Saving Time
        CST = GMT_6,                        // Central Standard Time
        CDT = GMT_5,                        // Central Daylight Saving Time
        MST = GMT_7,                        // Mountain Standard Time
        MDT = GMT_6,                        // Mountain Daylight Saving Time
        PST = GMT_8,                        // Pacific Standard Time
        PDT = GMT_7,                        // Pacific Daylight Saving Time
        HST = GMT_10,                       // Hawaiian Standard Time
        AKST = GMT_9,                       // Alaska Standard Time
        AKDT = GMT_8,                       // Alaska Daylight Saving Time

        // Australia

        A_WST = GMT8,                       // Western Standard Time
        A_CST = GMT13 + 1,                  // Central Standard Time (+9.5)
        A_EST = GMT10,                      // Eastern Standard Time
        A_ESST = GMT11,                     // Eastern Summer Time

        // New Zealand
        NZST = GMT12,                       // Standard Time
        NZDT = GMT13,                       // Daylight Saving Time
        
        // Universal Coordinated Time = the new and politically correct name
        // for GMT
        UTC = GMT0
    };
    

        // the calendar systems we know about: notice that it's valid (for
        // this classes purpose anyhow) to work with any of these calendars
        // even with the dates before the historical appearance of the
        // calendar
    enum Calendar
    {
        Gregorian,  // current calendar
        Julian      // calendar in use since -45 until the 1582 (or later)
    };



        // the country parameter is used so far for calculating the start and
        // the end of DST period and for deciding whether the date is a work
        // day or not
    enum Country
    {
        Country_Unknown, // no special information for this country
        Country_Default, // set the default country with SetCountry() method
                         // or use the default country with any other

        // Western European countries: we assume that they all follow the same
        // DST rules (True or False?)
        Country_WesternEurope_Start,
        Country_EEC = Country_WesternEurope_Start,
        France,
        Germany,
        UK,
        Country_WesternEurope_End = UK,

        Russia,

        USA
    };

        // symbolic names for the months
    enum Month
    {
        Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Inv_Month
    };

        // symbolic names for the weekdays
    enum WeekDay
    {
        Sun, Mon, Tue, Wed, Thu, Fri, Sat, Inv_WeekDay
    };

        // invalid value for the year
    enum Year
    {
        Inv_Year = SHRT_MIN    // should hold in wxDateTime_t
    };

        // flags for GetWeekDayName and GetMonthName
    enum NameFlags
    {
        Name_Full = 0x01,       // return full name
        Name_Abbr = 0x02        // return abbreviated name
    };

        // flags for GetWeekOfYear and GetWeekOfMonth
    enum WeekFlags
    {
        Default_First,   // Sunday_First for US, Monday_First for the rest
        Monday_First,    // week starts with a Monday
        Sunday_First     // week starts with a Sunday
    };


    //**  Nested class TimeZone is handled by a typemap instead
    
    //**  Is nested class Tm needed?
    
    
    // static methods
    // ------------------------------------------------------------------------

        // set the current country
    static void SetCountry(Country country);
    
        // get the current country
    static Country GetCountry();

        // return True if the country is a West European one (in practice,
        // this means that the same DST rules as for EEC apply)
    static bool IsWestEuropeanCountry(Country country = Country_Default);

        // return the current year
    static int GetCurrentYear(Calendar cal = Gregorian);

        // convert the year as returned by wxDateTime::GetYear() to a year
        // suitable for BC/AD notation. The difference is that BC year 1
        // corresponds to the year 0 (while BC year 0 didn't exist) and AD
        // year N is just year N.
    static int ConvertYearToBC(int year);

        // return the current month
    static Month GetCurrentMonth(Calendar cal = Gregorian);

        // returns True if the given year is a leap year in the given calendar
    static bool IsLeapYear(int year = Inv_Year, Calendar cal = Gregorian);

        // get the century (19 for 1999, 20 for 2000 and -5 for 492 BC)
    static int GetCentury(int year = Inv_Year);

        // returns the number of days in this year (356 or 355 for Gregorian
        // calendar usually :-)
    %Rename(GetNumberOfDaysinYear, 
        static wxDateTime_t, GetNumberOfDays(int year, Calendar cal = Gregorian));

        // get the number of the days in the given month (default value for
        // the year means the current one)
    %Rename(GetNumberOfDaysInMonth, 
        static wxDateTime_t, GetNumberOfDays(Month month,
                                            int year = Inv_Year,
                                            Calendar cal = Gregorian));

        // get the full (default) or abbreviated month name in the current
        // locale, returns empty string on error
    static wxString GetMonthName(Month month,
                                 NameFlags flags = Name_Full);

        // get the full (default) or abbreviated weekday name in the current
        // locale, returns empty string on error
    static wxString GetWeekDayName(WeekDay weekday,
                                   NameFlags flags = Name_Full);

        // get the standard English full (default) or abbreviated month name
    static wxString GetEnglishMonthName(Month month,
                                        NameFlags flags = Name_Full);

        // get the standard English full (default) or abbreviated weekday name
    static wxString GetEnglishWeekDayName(WeekDay weekday,
                                          NameFlags flags = Name_Full);

    %extend {
        DocAStr(
            GetAmPmStrings,
            "GetAmPmStrings() -> (am, pm)",
            "Get the AM and PM strings in the current locale (may be empty)", "");
        static PyObject* GetAmPmStrings() {
            wxString am;
            wxString pm;
            wxDateTime::GetAmPmStrings(&am, &pm);
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            PyObject* tup = PyTuple_New(2);
            PyTuple_SET_ITEM(tup, 0, wx2PyString(am));
            PyTuple_SET_ITEM(tup, 1, wx2PyString(pm));
            wxPyEndBlockThreads(blocked);
            return tup;
        }
    }
                
        // return True if the given country uses DST for this year
    static bool IsDSTApplicable(int year = Inv_Year,
                                Country country = Country_Default);

        // get the beginning of DST for this year, will return invalid object
        // if no DST applicable in this year. The default value of the
        // parameter means to take the current year.
    static wxDateTime GetBeginDST(int year = Inv_Year,
                                  Country country = Country_Default);
        // get the end of DST for this year, will return invalid object
        // if no DST applicable in this year. The default value of the
        // parameter means to take the current year.
    static wxDateTime GetEndDST(int year = Inv_Year,
                                Country country = Country_Default);

        // return the wxDateTime object for the current time
    static inline wxDateTime Now();

        // return the wxDateTime object for the current time with millisecond
        // precision (if available on this platform)
    static wxDateTime UNow();

        // return the wxDateTime object for today midnight: i.e. as Now() but
        // with time set to 0
    static inline wxDateTime Today();



    // ------------------------------------------------------------------------
    // constructors

    wxDateTime();
    %RenameCtor(DateTimeFromTimeT, wxDateTime(time_t timet));
    %RenameCtor(DateTimeFromJDN, wxDateTime(double jdn));
    %RenameCtor(DateTimeFromHMS, wxDateTime(wxDateTime_t hour,
                                     wxDateTime_t minute = 0,
                                     wxDateTime_t second = 0,
                                     wxDateTime_t millisec = 0));
    %RenameCtor(DateTimeFromDMY, wxDateTime(wxDateTime_t day,
                                     Month        month = Inv_Month,
                                     int          year = Inv_Year,
                                     wxDateTime_t hour = 0,
                                     wxDateTime_t minute = 0,
                                     wxDateTime_t second = 0,
                                     wxDateTime_t millisec = 0));
    %RenameCtor(DateTimeFromDateTime, wxDateTime(const wxDateTime& date));
            
    ~wxDateTime();

    // ------------------------------------------------------------------------
    // Set methods

    // This typemap ensures that the returned object is the same
    // Python instance as what was passed in as `self`, instead of
    // creating a new proxy as SWIG would normally do.
    %typemap(out) wxDateTime& { $result = $self; Py_INCREF($result); }
    
    wxDateTime& SetToCurrent();

        // set to given time_t value
    %Rename(SetTimeT, wxDateTime&, Set(time_t timet));

        // set to given JDN (beware of rounding errors)
    %Rename(SetJDN, wxDateTime&, Set(double jdn));

        // set to given time, date = today
    %Rename(SetHMS, wxDateTime&, Set(wxDateTime_t hour,
                    wxDateTime_t minute = 0,
                    wxDateTime_t second = 0,
                    wxDateTime_t millisec = 0));

        // from separate values for each component with explicit date
        // (defaults for month and year are the current values)
    wxDateTime& Set(wxDateTime_t day,
                    Month        month = Inv_Month,
                    int          year = Inv_Year, // 1999, not 99 please!
                    wxDateTime_t hour = 0,
                    wxDateTime_t minute = 0,
                    wxDateTime_t second = 0,
                    wxDateTime_t millisec = 0);

        // resets time to 00:00:00, doesn't change the date
    wxDateTime& ResetTime();

        // get the date part of this object only, i.e. the object which has the
        // same date as this one but time of 00:00:00
    wxDateTime GetDateOnly() const;
    
        // the following functions don't change the values of the other
        // fields, i.e. SetMinute() won't change either hour or seconds value

        // set the year
    wxDateTime& SetYear(int year);
        // set the month
    wxDateTime& SetMonth(Month month);
        // set the day of the month
    wxDateTime& SetDay(wxDateTime_t day);
        // set hour
    wxDateTime& SetHour(wxDateTime_t hour);
        // set minute
    wxDateTime& SetMinute(wxDateTime_t minute);
        // set second
    wxDateTime& SetSecond(wxDateTime_t second);
        // set millisecond
    wxDateTime& SetMillisecond(wxDateTime_t millisecond);


    // ------------------------------------------------------------------------
    // calendar calculations

        // set to the given week day in the same week as this one
    wxDateTime& SetToWeekDayInSameWeek(WeekDay weekday, WeekFlags flags = Monday_First);
    wxDateTime GetWeekDayInSameWeek(WeekDay weekday, WeekFlags flags = Monday_First);

        // set to the next week day following this one
    wxDateTime& SetToNextWeekDay(WeekDay weekday);
    wxDateTime GetNextWeekDay(WeekDay weekday);

        // set to the previous week day before this one
    wxDateTime& SetToPrevWeekDay(WeekDay weekday);
    wxDateTime GetPrevWeekDay(WeekDay weekday);

        // set to Nth occurence of given weekday in the given month of the
        // given year (time is set to 0), return True on success and False on
        // failure. n may be positive (1..5) or negative to count from the end
        // of the month (see helper function SetToLastWeekDay())
    bool SetToWeekDay(WeekDay weekday,
                      int n = 1,
                      Month month = Inv_Month,
                      int year = Inv_Year);

        // sets to the last weekday in the given month, year
    bool SetToLastWeekDay(WeekDay weekday,
                          Month month = Inv_Month,
                          int year = Inv_Year);
    wxDateTime GetLastWeekDay(WeekDay weekday,
                              Month month = Inv_Month,
                              int year = Inv_Year);

        // returns the date corresponding to the given week day of the given
        // week (in ISO notation) of the specified year
    static wxDateTime SetToWeekOfYear(int year,
                                      wxDateTime_t numWeek,
                                      WeekDay weekday = Mon);
    
        // sets the date to the last day of the given (or current) month or the
        // given (or current) year
    wxDateTime& SetToLastMonthDay(Month month = Inv_Month,
                                  int year = Inv_Year);
    wxDateTime GetLastMonthDay(Month month = Inv_Month,
                               int year = Inv_Year);

        // sets to the given year day (1..365 or 366)
    wxDateTime& SetToYearDay(wxDateTime_t yday);
    wxDateTime GetYearDay(wxDateTime_t yday);

        // The definitions below were taken verbatim from
        //
        //      http://www.capecod.net/~pbaum/date/date0.htm
        //
        // (Peter Baum's home page)
        //
        // definition: The Julian Day Number, Julian Day, or JD of a
        // particular instant of time is the number of days and fractions of a
        // day since 12 hours Universal Time (Greenwich mean noon) on January
        // 1 of the year -4712, where the year is given in the Julian
        // proleptic calendar. The idea of using this reference date was
        // originally proposed by Joseph Scalizer in 1582 to count years but
        // it was modified by 19th century astronomers to count days. One
        // could have equivalently defined the reference time to be noon of
        // November 24, -4713 if were understood that Gregorian calendar rules
        // were applied. Julian days are Julian Day Numbers and are not to be
        // confused with Julian dates.
        //
        // definition: The Rata Die number is a date specified as the number
        // of days relative to a base date of December 31 of the year 0. Thus
        // January 1 of the year 1 is Rata Die day 1.

        // get the Julian Day number (the fractional part specifies the time of
        // the day, related to noon - beware of rounding errors!)
    double GetJulianDayNumber();
    double GetJDN();

        // get the Modified Julian Day number: it is equal to JDN - 2400000.5
        // and so integral MJDs correspond to the midnights (and not noons).
        // MJD 0 is Nov 17, 1858
    double GetModifiedJulianDayNumber() const { return GetJDN() - 2400000.5; }
    double GetMJD();

        // get the Rata Die number
    double GetRataDie();


    // ------------------------------------------------------------------------
    // timezone stuff

        // transform to any given timezone
    wxDateTime ToTimezone(const wxDateTime::TimeZone& tz, bool noDST = false);
    wxDateTime& MakeTimezone(const wxDateTime::TimeZone& tz, bool noDST = false);

        // interpret current value as being in another timezone and transform
        // it to local one
    wxDateTime FromTimezone(const wxDateTime::TimeZone& tz, bool noDST = false) const;
    wxDateTime& MakeFromTimezone(const wxDateTime::TimeZone& tz, bool noDST = false);

        // transform to/from GMT/UTC
    wxDateTime ToUTC(bool noDST = false) const;
    wxDateTime& MakeUTC(bool noDST = false);

    wxDateTime ToGMT(bool noDST = false) const;
    wxDateTime& MakeGMT(bool noDST = false);

    wxDateTime FromUTC(bool noDST = false) const;
    wxDateTime& MakeFromUTC(bool noDST = false);

    
        // is daylight savings time in effect at this moment according to the
        // rules of the specified country?
        //
        // Return value is > 0 if DST is in effect, 0 if it is not and -1 if
        // the information is not available (this is compatible with ANSI C)
    int IsDST(Country country = Country_Default);

    // Clear the typemap
    %typemap(out) wxDateTime& ;


    // ------------------------------------------------------------------------
    // accessors

        // is the date valid (True even for non initialized objects)?
    inline bool IsValid() const;
    %pythoncode { IsOk = IsValid }
    %pythoncode { Ok = IsOk }
   
    %pythoncode { def __nonzero__(self): return self.IsOk() };

    
        // get the number of seconds since the Unix epoch - returns (time_t)-1
        // if the value is out of range
    inline time_t GetTicks() const;

        // get the year (returns Inv_Year if date is invalid)
    int GetYear(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the month (Inv_Month if date is invalid)
    Month GetMonth(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the month day (in 1..31 range, 0 if date is invalid)
    wxDateTime_t GetDay(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the day of the week (Inv_WeekDay if date is invalid)
    WeekDay GetWeekDay(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the hour of the day
    wxDateTime_t GetHour(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the minute
    wxDateTime_t GetMinute(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get the second
    wxDateTime_t GetSecond(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // get milliseconds
    wxDateTime_t GetMillisecond(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;


        // get the day since the year start (1..366, 0 if date is invalid)
    wxDateTime_t GetDayOfYear(const wxDateTime::TimeZone& tz = LOCAL_TZ) const;
        // get the week number since the year start (1..52 or 53, 0 if date is
        // invalid)
    wxDateTime_t GetWeekOfYear(WeekFlags flags = Monday_First,
                               const wxDateTime::TimeZone& tz = LOCAL_TZ) const;
        // get the week number since the month start (1..5, 0 if date is
        // invalid)
    wxDateTime_t GetWeekOfMonth(WeekFlags flags = Monday_First,
                                const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // is this date a work day? This depends on a country, of course,
        // because the holidays are different in different countries
    bool IsWorkDay(Country country = Country_Default) const;



    // ------------------------------------------------------------------------
    // comparison (see also functions below for operator versions)

        // returns True if the two moments are strictly identical
    inline bool IsEqualTo(const wxDateTime& datetime) const;

        // returns True if the date is strictly earlier than the given one
    inline bool IsEarlierThan(const wxDateTime& datetime) const;

        // returns True if the date is strictly later than the given one
    inline bool IsLaterThan(const wxDateTime& datetime) const;

        // returns True if the date is strictly in the given range
    inline bool IsStrictlyBetween(const wxDateTime& t1,
                                  const wxDateTime& t2) const;

        // returns True if the date is in the given range
    inline bool IsBetween(const wxDateTime& t1, const wxDateTime& t2) const;

        // do these two objects refer to the same date?
    inline bool IsSameDate(const wxDateTime& dt) const;

        // do these two objects have the same time?
    inline bool IsSameTime(const wxDateTime& dt) const;

        // are these two objects equal up to given timespan?
    inline bool IsEqualUpTo(const wxDateTime& dt, const wxTimeSpan& ts) const;


    // ------------------------------------------------------------------------
    // arithmetics with dates (see also below for more operators)

        // add a time span (positive or negative)
    %Rename(AddTS,  wxDateTime&, Add(const wxTimeSpan& diff));
        // add a date span (positive or negative)
    %Rename(AddDS,  wxDateTime&, Add(const wxDateSpan& diff));

        // subtract a time span (positive or negative)
    %Rename(SubtractTS,  wxDateTime&, Subtract(const wxTimeSpan& diff));

        // subtract a date span (positive or negative)
    %Rename(SubtractDS,  wxDateTime&, Subtract(const wxDateSpan& diff));

        // return the difference between two dates
    wxTimeSpan Subtract(const wxDateTime& dt) const;


    %nokwargs operator+=;
        // add a time span (positive or negative)
    inline wxDateTime& operator+=(const wxTimeSpan& diff);
        // add a date span (positive or negative)
    inline wxDateTime& operator+=(const wxDateSpan& diff);

    %nokwargs operator-=;
        // subtract a time span (positive or negative)
    inline wxDateTime& operator-=(const wxTimeSpan& diff);
        // subtract a date span (positive or negative)
    inline wxDateTime& operator-=(const wxDateSpan& diff);


//     inline bool operator<(const wxDateTime& dt) const;
//     inline bool operator<=(const wxDateTime& dt) const;
//     inline bool operator>(const wxDateTime& dt) const;
//     inline bool operator>=(const wxDateTime& dt) const;
//     inline bool operator==(const wxDateTime& dt) const;
//     inline bool operator!=(const wxDateTime& dt) const;

    %nokwargs __add__;
    %nokwargs __sub__;
    %extend {
        wxDateTime __add__(const wxTimeSpan& other) { return *self + other; }
        wxDateTime __add__(const wxDateSpan& other) { return *self + other; }

        wxTimeSpan __sub__(const wxDateTime& other) { return *self - other; }
        wxDateTime __sub__(const wxTimeSpan& other) { return *self - other; }
        wxDateTime __sub__(const wxDateSpan& other) { return *self - other; }

        // These fall back to just comparing pointers if other is NULL, or if
        // either operand is invalid.  This allows Python comparrisons to None
        // to not assert and to return a sane value for the compare.
        bool __lt__(const wxDateTime* other) { 
            if (!other || !self->IsValid() || !other->IsValid()) return self <  other; 
            return (*self <  *other);
        }
        bool __le__(const wxDateTime* other) { 
            if (!other || !self->IsValid() || !other->IsValid()) return self <= other; 
            return (*self <= *other);
        }
        bool __gt__(const wxDateTime* other) { 
            if (!other || !self->IsValid() || !other->IsValid()) return self >  other; 
            return (*self >  *other);
        }
        bool __ge__(const wxDateTime* other) { 
            if (!other || !self->IsValid() || !other->IsValid()) return self >= other; 
            return (*self >= *other);
        }

        bool __eq__(const wxDateTime* other) {
            if (!other || !self->IsValid() || !other->IsValid()) return self == other; 
            return (*self == *other);
        }
        bool __ne__(const wxDateTime* other) {
            if (!other || !self->IsValid() || !other->IsValid()) return self != other; 
            return (*self != *other);
        }            
    }

   
    %extend {
        // parse a string in RFC 822 format (found e.g. in mail headers and
        // having the form "Wed, 10 Feb 1999 19:07:07 +0100")
        int ParseRfc822Date(const wxString& date)
        {
            wxString::const_iterator begin = date.begin();
            wxString::const_iterator end;
            if (!self->ParseRfc822Date(date, &end))
                return -1;
            return end - begin;
        }

        // parse a date/time in the given format (see strptime(3)), fill in
        // the missing (in the string) fields with the values of dateDef (by
        // default, they will not change if they had valid values or will
        // default to Today() otherwise)
        int ParseFormat(const wxString& date,
                         const wxString& format = wxPyDefaultDateTimeFormat,
                         const wxDateTime& dateDef = wxDefaultDateTime)
        {
            wxString::const_iterator begin = date.begin();
            wxString::const_iterator end;
            if (!self->ParseFormat(date, format, dateDef, &end))
                return -1;
            return end - begin;
        }
    }

    
    // parse a string containing date, time or both in ISO 8601 format
    //
    // notice that these functions are new in wx 3.0 and so we don't
    // provide compatibility overloads for them
    bool ParseISODate(const wxString& date);
    bool ParseISOTime(const wxString& time);
    bool ParseISOCombined(const wxString& datetime, char sep = 'T');


    %extend {
        // parse a string containing the date/time in "free" format, this
        // function will try to make an educated guess at the string contents
        int ParseDateTime(const wxString& datetime)
        {
            wxString::const_iterator begin = datetime.begin();
            wxString::const_iterator end;
            if (!self->ParseDateTime(datetime, &end))
                return -1;
            return end - begin;
        }

        // parse a string containing the date only in "free" format (less
        // flexible than ParseDateTime)
        int ParseDate(const wxString& date)
        {
            wxString::const_iterator begin = date.begin();
            wxString::const_iterator end;
            if (!self->ParseDate(date, &end))
                return -1;
            return end - begin;
        }
            
        // parse a string containing the time only in "free" format
        // bool ParseTime(const wxString& time)
        // {
        //     wxString::const_iterator end;
        //     return self->ParseTime(time, &end);
        // }

        int ParseTime(const wxString& time)
        {
            wxString::const_iterator begin = time.begin();
            wxString::const_iterator end;
            if (!self->ParseTime(time, &end))
                return -1;
            return end - begin;
        }
    }

        // this function accepts strftime()-like format string (default
        // argument corresponds to the preferred date and time representation
        // for the current locale) and returns the string containing the
        // resulting text representation
    wxString Format(const wxString& format = wxPyDefaultDateTimeFormat,
                    const wxDateTime::TimeZone& tz = LOCAL_TZ) const;

        // preferred date representation for the current locale
    wxString FormatDate() const;

        // preferred time representation for the current locale
    wxString FormatTime() const;

        // returns the string representing the date in ISO 8601 format
        // (YYYY-MM-DD)
    wxString FormatISODate() const;

        // returns the string representing the time in ISO 8601 format
        // (HH:MM:SS)
    wxString FormatISOTime() const;

        // return the combined date time representation in ISO 8601 format; the
        // separator character should be 'T' according to the standard but it
        // can also be useful to set it to ' '
    wxString FormatISOCombined(char sep = 'T') const;
    
    %pythoncode {
    def __repr__(self):
        if self.IsValid():
            f = self.Format().encode(wx.GetDefaultPyEncoding())
            return '<wx.DateTime: \"%s\" at %s>' % ( f, self.this)
        else:
            return '<wx.DateTime: \"INVALID\" at %s>' % self.this
    def __str__(self):
        if self.IsValid():
            return self.Format().encode(wx.GetDefaultPyEncoding())
        else:
            return "INVALID DateTime"
    }

    %property(Day, GetDay, SetDay, doc="See `GetDay` and `SetDay`");
    %property(DayOfYear, GetDayOfYear, doc="See `GetDayOfYear`");
    %property(Hour, GetHour, SetHour, doc="See `GetHour` and `SetHour`");
    %property(JDN, GetJDN, SetJDN, doc="See `GetJDN` and `SetJDN`");
    %property(JulianDayNumber, GetJulianDayNumber, doc="See `GetJulianDayNumber`");
    %property(LastMonthDay, GetLastMonthDay, doc="See `GetLastMonthDay`");
    %property(LastWeekDay, GetLastWeekDay, doc="See `GetLastWeekDay`");
    %property(MJD, GetMJD, doc="See `GetMJD`");
    %property(Millisecond, GetMillisecond, SetMillisecond, doc="See `GetMillisecond` and `SetMillisecond`");
    %property(Minute, GetMinute, SetMinute, doc="See `GetMinute` and `SetMinute`");
    %property(ModifiedJulianDayNumber, GetModifiedJulianDayNumber, doc="See `GetModifiedJulianDayNumber`");
    %property(Month, GetMonth, SetMonth, doc="See `GetMonth` and `SetMonth`");
    %property(NextWeekDay, GetNextWeekDay, doc="See `GetNextWeekDay`");
    %property(PrevWeekDay, GetPrevWeekDay, doc="See `GetPrevWeekDay`");
    %property(RataDie, GetRataDie, doc="See `GetRataDie`");
    %property(Second, GetSecond, SetSecond, doc="See `GetSecond` and `SetSecond`");
    %property(Ticks, GetTicks, doc="See `GetTicks`");
    %property(WeekDay, GetWeekDay, doc="See `GetWeekDay`");
    %property(WeekDayInSameWeek, GetWeekDayInSameWeek, doc="See `GetWeekDayInSameWeek`");
    %property(WeekOfMonth, GetWeekOfMonth, doc="See `GetWeekOfMonth`");
    %property(WeekOfYear, GetWeekOfYear, doc="See `GetWeekOfYear`");
    %property(Year, GetYear, SetYear, doc="See `GetYear` and `SetYear`");
    %property(YearDay, GetYearDay, doc="See `GetYearDay`");
    
};

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------


// This class contains a difference between 2 wxDateTime values, so it makes
// sense to add it to wxDateTime and it is the result of subtraction of 2
// objects of that class. See also wxDateSpan.
class wxTimeSpan
{
public:

    // TODO:  Need an input typemap for wxLongLong...
    
    
        // return the timespan for the given number of milliseconds
    static wxTimeSpan Milliseconds(/*wxLongLong*/ long ms);
    static wxTimeSpan Millisecond(); 
    
        // return the timespan for the given number of seconds
    static wxTimeSpan Seconds(/*wxLongLong*/ long sec);
    static wxTimeSpan Second();

        // return the timespan for the given number of minutes
    static wxTimeSpan Minutes(long min);
    static wxTimeSpan Minute();

        // return the timespan for the given number of hours
    static wxTimeSpan Hours(long hours);
    static wxTimeSpan Hour();

        // return the timespan for the given number of days
    static wxTimeSpan Days(long days);
    static wxTimeSpan Day();

        // return the timespan for the given number of weeks
    static wxTimeSpan Weeks(long days);
    static wxTimeSpan Week();

    // ------------------------------------------------------------------------
    // constructors

        // from separate values for each component, date set to 0 (hours are
        // not restricted to 0..24 range, neither are minutes, seconds or
        // milliseconds)
    wxTimeSpan(long hours = 0,
               long minutes = 0,
               /*wxLongLong*/ long seconds = 0,
               /*wxLongLong*/ long milliseconds = 0);

    ~wxTimeSpan();

    // ------------------------------------------------------------------------
    // arithmetics with time spans

    // This typemap ensures that the returned object is the same
    // Python instance as what was passed in as `self`, instead of
    // creating a new proxy as SWIG would normally do.
    %typemap(out) wxTimeSpan& { $result = $self; Py_INCREF($result); }

        // add two timespans together
    inline wxTimeSpan& Add(const wxTimeSpan& diff);

        // subtract another timespan
    inline wxTimeSpan& Subtract(const wxTimeSpan& diff);

        // multiply timespan by a scalar
    inline wxTimeSpan& Multiply(int n);

        // negate the value of the timespan
    wxTimeSpan& Neg();

        // return the absolute value of the timespan: does _not_ modify the
        // object
    inline wxTimeSpan Abs() const;

    
    wxTimeSpan& operator+=(const wxTimeSpan& diff);
    wxTimeSpan& operator-=(const wxTimeSpan& diff);
    wxTimeSpan& operator*=(int n);
    wxTimeSpan& operator-();

    // Clear the typemap
    %typemap(out) wxTimeSpan& ;
    
    %extend {
        wxTimeSpan __add__(const wxTimeSpan& other) { return *self + other; }
        wxTimeSpan __sub__(const wxTimeSpan& other) { return *self - other; }
        wxTimeSpan __mul__(int n)                   { return *self * n; }
        wxTimeSpan __rmul__(int n)                  { return n * *self; }
        
        bool __lt__(const wxTimeSpan* other) { return other ? (*self <  *other) : false; }
        bool __le__(const wxTimeSpan* other) { return other ? (*self <= *other) : false; }
        bool __gt__(const wxTimeSpan* other) { return other ? (*self >  *other) : true;  }
        bool __ge__(const wxTimeSpan* other) { return other ? (*self >= *other) : true;  }
        bool __eq__(const wxTimeSpan* other) { return other ? (*self == *other) : false; }
        bool __ne__(const wxTimeSpan* other) { return other ? (*self != *other) : true;  }
    }



    // ------------------------------------------------------------------------
   
        // is the timespan null?
    bool IsNull() const;

        // is the timespan positive?
    bool IsPositive() const;

        // is the timespan negative?
    bool IsNegative() const;

        // are two timespans equal?
    inline bool IsEqualTo(const wxTimeSpan& ts) const;

        // compare two timestamps: works with the absolute values, i.e. -2
        // hours is longer than 1 hour. Also, it will return False if the
        // timespans are equal in absolute value.
    inline bool IsLongerThan(const wxTimeSpan& ts) const;

        // compare two timestamps: works with the absolute values, i.e. 1
        // hour is shorter than -2 hours. Also, it will return False if the
        // timespans are equal in absolute value.
    bool IsShorterThan(const wxTimeSpan& t) const;

    // ------------------------------------------------------------------------
    // breaking into days, hours, minutes and seconds

        // get the max number of weeks in this timespan
    inline int GetWeeks() const;
        // get the max number of days in this timespan
    inline int GetDays() const;
        // get the max number of hours in this timespan
    inline int GetHours() const;
        // get the max number of minutes in this timespan
    inline int GetMinutes() const;


         // get the max number of seconds in this timespan
    inline wxLongLong GetSeconds() const;
         // get the number of milliseconds in this timespan
    wxLongLong GetMilliseconds() const;

    // ------------------------------------------------------------------------
    // conversion to text

        // this function accepts strftime()-like format string (default
        // argument corresponds to the preferred date and time representation
        // for the current locale) and returns the string containing the
        // resulting text representation. Notice that only some of format
        // specifiers valid for wxDateTime are valid for wxTimeSpan: hours,
        // minutes and seconds make sense, but not "PM/AM" string for example.
    wxString Format(const wxString& format = wxPyDefaultTimeSpanFormat) const;

    %pythoncode {
     def __repr__(self):
         f = self.Format().encode(wx.GetDefaultPyEncoding())
         return '<wx.TimeSpan: \"%s\" at %s>' % ( f, self.this)
     def __str__(self):
         return self.Format().encode(wx.GetDefaultPyEncoding())
     }

    %property(days, GetDays, doc="See `GetDays`");
    %property(hours, GetHours, doc="See `GetHours`");
    %property(milliseconds, GetMilliseconds, doc="See `GetMilliseconds`");
    %property(minutes, GetMinutes, doc="See `GetMinutes`");
    %property(seconds, GetSeconds, doc="See `GetSeconds`");
    %property(weeks, GetWeeks, doc="See `GetWeeks`");
};


//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

// This class is a "logical time span" and is useful for implementing program
// logic for such things as "add one month to the date" which, in general,
// doesn't mean to add 60*60*24*31 seconds to it, but to take the same date
// the next month (to understand that this is indeed different consider adding
// one month to Feb, 15 - we want to get Mar, 15, of course).
//
// When adding a month to the date, all lesser components (days, hours, ...)
// won't be changed unless the resulting date would be invalid: for example,
// Jan 31 + 1 month will be Feb 28, not (non existing) Feb 31.
//
// Because of this feature, adding and subtracting back again the same
// wxDateSpan will *not*, in general give back the original date: Feb 28 - 1
// month will be Jan 28, not Jan 31!
//
// wxDateSpan can be either positive or negative. They may be
// multiplied by scalars which multiply all deltas by the scalar: i.e. 2*(1
// month and 1 day) is 2 months and 2 days. They can be added together and
// with wxDateTime or wxTimeSpan, but the type of result is different for each
// case.
//
// Beware about weeks: if you specify both weeks and days, the total number of
// days added will be 7*weeks + days! See also GetTotalDays() function.
//
// Equality operators are defined for wxDateSpans. Two datespans are equal if
// they both give the same target date when added to *every* source date.
// Thus wxDateSpan::Months(1) is not equal to wxDateSpan::Days(30), because
// they not give the same date when added to 1 Feb. But wxDateSpan::Days(14) is
// equal to wxDateSpan::Weeks(2)
//
// Finally, notice that for adding hours, minutes &c you don't need this
// class: wxTimeSpan will do the job because there are no subtleties
// associated with those.
class wxDateSpan
{
public:
        // this many years/months/weeks/days
    wxDateSpan(int years = 0, int months = 0, int weeks = 0, int days = 0)
    {
        m_years = years;
        m_months = months;
        m_weeks = weeks;
        m_days = days;
    }

    ~wxDateSpan();

        // get an object for the given number of days
    static wxDateSpan Days(int days);
    static wxDateSpan Day();

        // get an object for the given number of weeks
    static wxDateSpan Weeks(int weeks);
    static wxDateSpan Week();

        // get an object for the given number of months
    static wxDateSpan Months(int mon);
    static wxDateSpan Month();

        // get an object for the given number of years
    static wxDateSpan Years(int years);
    static wxDateSpan Year();


    // ------------------------------------------------------------------------

    // This typemap ensures that the returned object is the same
    // Python instance as what was passed in as `self`, instead of
    // creating a new proxy as SWIG would normally do.
    %typemap(out) wxDateSpan& { $result = $self; Py_INCREF($result); }

        // set number of years
    wxDateSpan& SetYears(int n);
        // set number of months
    wxDateSpan& SetMonths(int n);
        // set number of weeks
    wxDateSpan& SetWeeks(int n);
        // set number of days
    wxDateSpan& SetDays(int n);

        // get number of years
    int GetYears() const;
        // get number of months
    int GetMonths() const;
        // get number of weeks
    int GetWeeks() const;
        // get number of days
    int GetDays() const;
        // returns 7*GetWeeks() + GetDays()
    int GetTotalDays() const;


    // ------------------------------------------------------------------------

        // add another wxDateSpan to us
    inline wxDateSpan& Add(const wxDateSpan& other);

        // subtract another wxDateSpan from us
    inline wxDateSpan& Subtract(const wxDateSpan& other);

        // inverse the sign of this timespan
    inline wxDateSpan& Neg();

        // multiply all components by a (signed) number
    inline wxDateSpan& Multiply(int factor);

    inline wxDateSpan& operator+=(const wxDateSpan& other);
    inline wxDateSpan& operator-=(const wxDateSpan& other);
    wxDateSpan& operator-() { return Neg(); }
    inline wxDateSpan& operator*=(int factor) { return Multiply(factor); }

    // Clear the typemap
    %typemap(out) wxDateSpan& ;
    
    %extend {
        wxDateSpan __add__(const wxDateSpan& other) { return *self + other; }
        wxDateSpan __sub__(const wxDateSpan& other) { return *self - other; }
        wxDateSpan __mul__(int n)                   { return *self * n; }
        wxDateSpan __rmul__(int n)                  { return n * *self; }
        
//         bool __lt__(const wxDateSpan* other) { return other ? (*self <  *other) : false; }
//         bool __le__(const wxDateSpan* other) { return other ? (*self <= *other) : false; }
//         bool __gt__(const wxDateSpan* other) { return other ? (*self >  *other) : true;  }
//         bool __ge__(const wxDateSpan* other) { return other ? (*self >= *other) : true;  }
        
        bool __eq__(const wxDateSpan* other) { return other ? (*self == *other) : false; }
        bool __ne__(const wxDateSpan* other) { return other ? (*self != *other) : true;  }
    }

    %property(days, GetDays, SetDays, doc="See `GetDays` and `SetDays`");
    %property(months, GetMonths, SetMonths, doc="See `GetMonths` and `SetMonths`");
    %property(totalDays, GetTotalDays, doc="See `GetTotalDays`");
    %property(weeks, GetWeeks, SetWeeks, doc="See `GetWeeks` and `SetWeeks`");
    %property(years, GetYears, SetYears, doc="See `GetYears` and `SetYears`");
};


//---------------------------------------------------------------------------

// TODO: wxDateTimeHolidayAuthority

//---------------------------------------------------------------------------

long wxGetLocalTime();
long wxGetUTCTime();
long wxGetCurrentTime();
wxLongLong wxGetLocalTimeMillis();

%immutable;
const wxDateTime        wxDefaultDateTime;
%mutable;

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
