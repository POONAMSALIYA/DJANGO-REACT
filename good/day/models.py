from django.db import models

# Create your models here.
hey do the commit
import React, { useState, useEffect } from "react";
import Box from '@mui/material/Box';
import LocalLaundryServiceIcon from '@mui/icons-material/LocalLaundryService';
import CellWifiIcon from '@mui/icons-material/CellWifi';
import IconButton from '@mui/material/IconButton';
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import SoupKitchenIcon from '@mui/icons-material/SoupKitchen';
import {
    Button,
    Typography,
    Grid,
    Backdrop,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    TextField,
    DialogTitle,
    Container,
    CardContent,
    Card,
    Divider,
    Link,
    useMediaQuery,
    useTheme
} from "@mui/material";

import { Link as RouterLink } from "react-router-dom";
// import { useTheme } from '@mui/material/styles';
import axios from "api/axios";
import CustomSnackbar from "components/Snackbar";
import CustomErrorBox from "components/ErrorAlert";
import ItemCard from "components/cards/statistics/ItemCard";
import LateCheckoutDatagrid from "pages/bookings/LateCheckoutDatagrid";

const CustomerBooking = ({uuid, handleCustomerExistState}) => {
    const theme = useTheme();
    const matchesSM = useMediaQuery(theme.breakpoints.down('sm'));
    const BOOKING_URL = `/bookings`;
    const [booking, setBooking] = useState(null);
    // To show major errors
    const [error, setError] = useState("");
    const [isDataLoading, setIsDataLoading] = useState(true);
    // Whether CheckIn should be allowed at this time or not
    const [showCheckIn, setShowCheckIn] = useState(true);
    // To store Late Checkout request data
    const [lateDateTime, setLateDateTime] = useState({ 
        requested_checkout_time : "",
        requested_end_date : "",
    });
    // To show late checkout request form
    const [showLateDateTimeForm, setShowLateDateTimeForm] = useState(false);
    // To show error messages in snackbar
    const [errorMessage, setErrorMessage] = useState("");
    // To show success messages in snackbar
    const [successMessage, setSuccessMessage] = useState("");

    function checkInAvailable(checkInDate, checkInTime) {
        // Function to Calculate that check In button should be displayed or not
        // Get the current date and time
        const currentDate = new Date();
        const currentDateTime = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            currentDate.getDate(),
            currentDate.getHours(),
            currentDate.getMinutes()
        );

        // Get the check-in date and time
        const checkInDateTime = new Date(checkInDate + " " + checkInTime);

        // Add 30 minutes to the current date and time
        const checkInTimePlus30Minutes = new Date(
            currentDateTime.getTime() + 1000 * 60 * 30
        );
        
        // Check if the current date and time plus 30 minutes is earlier than the check-in date and time
        if (checkInTimePlus30Minutes < checkInDateTime) {
            return true;
        }

        // If the current date and time plus 30 minutes is equal to or greater than the check-in date and time, the check-in is not available
        return false;
    }

    async function fetchData1() {
        try {
            const response = await axios.get(BOOKING_URL + `/${uuid}`);
            setBooking(response.data);
            setShowCheckIn(checkInAvailable(response.data?.start_date,response.data?.checkin_time));
            setIsDataLoading(false);
        } catch (error) {
            console.error(error);
            if(error.response?.data?.detail){
                setError(error.response.data.detail);
            }
            else {
                setError("Failed to fetch booking details. Please try again!");
            }
            setIsDataLoading(false);
        }
    }
    async function customerCheckIn() {
        try {
            const response = await axios.patch(
                BOOKING_URL + `/${uuid}/check-in`
            );
            console.log("CheckIn booking: ", response.data);
            setIsDataLoading(true);
            fetchData1();
        } catch (error) {
            console.error(error);
            if(error.response?.data?.detail){
                setError(error.response.data.detail);
            }
            else {
                setError("Error Check In Booking. Please try again!");
            }
        }
    }
    function formatDate(inputDate) {
        const date = new Date(inputDate);
        const options = {
            weekday: 'long',
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        };
        return date.toLocaleDateString('en-US', options);
    }
    async function customerCheckOut() {
        try {
            const response = await axios.patch(
                BOOKING_URL + `/${uuid}/check-out`
            );
            console.log("CheckOut booking: ", response.data);
            setIsDataLoading(true);
            fetchData1();
            // Move the Customer to Next Step, i.e. Feedback
            handleCustomerExistState(3);
        } catch (error) {
            console.error(error);
            if(error.response?.data?.detail){
                setError(error.response.data.detail);
            }
            else {
                setError("Error Check Out Booking. Please try again!");
            }
        }
    }
    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get(BOOKING_URL + `/${uuid}`);
                setBooking(response.data);
                setShowCheckIn(checkInAvailable(response.data?.start_date,response.data?.checkin_time));
                setIsDataLoading(false);
            } catch (error) {
                console.error(error);
                if(error.response?.data?.detail){
                    setError(error.response.data.detail);
                }
                else {
                    setError("Failed to fetch booking details. Please try again!");
                }
                setIsDataLoading(false);
            }
        }
        fetchData();
    }, [uuid, BOOKING_URL]);

    const handleLateCheckoutButtonClick = async (event) => {
        event.preventDefault();
          try {
            const response = await axios.post(`/bookings/create-late-checkout-request/${uuid}/`, lateDateTime);
            console.log("Late CheckOut Success: ",response.data);
            setLateDateTime({ 
                requested_checkout_time : "",
                requested_end_date : "",
            });
            
            setErrorMessage("");
            setShowLateDateTimeForm(false);
            setSuccessMessage("Late CheckOut Request Successful!");
            fetchData1();
          }
          catch (e) {
            if(e.response?.data?.detail) {
                setErrorMessage(e.response.data.detail)
            }
            else {
                
                setErrorMessage("Late Request Failed!")
            }
            setShowLateDateTimeForm(false);
          }
      };
    
      const handleCancelLateCheckoutButtonClick = () => {
        setShowLateDateTimeForm(false);
        setLateDateTime({ 
            requested_checkout_time : "",
            requested_end_date : "",
        });
      };
    
      const handleLateCheckoutInputChange = (e) => {
        setLateDateTime({ ...lateDateTime, [e.target.name]: e.target.value });
      };

    return isDataLoading ? (
        <Backdrop
            open={isDataLoading}
            sx={{
                color: "#fff",
                zIndex: (theme) => theme.zIndex.drawer + 1,
            }}
        >
            <CircularProgress color="inherit" />
        </Backdrop>
    ) : !error && booking ? (
        <>
            
                <Typography variant="h4" gutterBottom sx={{ marginBottom: '30px', fontWeight: 800}} >
                    Booking Details
                </Typography>
                {/* Booking Details Cards */}
                <Container maxWidth="sm">




                <Card sx={{border: "solid 1px #bbb", marginBottom: "2rem"}}>
                        <CardContent>
                            <Grid container spacing={3} >


   <Box sx={{ width: 600, height: 500, bgcolor: 'background.paper', display: 'flex', flexDirection: 'column', marginRight: '0px',boxShadow: '0px 0px 0px rgba(0, 1, 1, 1)',marginLeft:'-50px' }}>
   <Box sx={{ width: '85%', height: '60%', overflow: 'hidden',marginLeft:'155px', marginTop: '20px' }}>
         <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGhMHjX1oBHOlxtx7sjZaah2tU-oFUpyThiw&s" alt="Hotel room" style={{  width: '85%', height: '60%', marginLeft:'0px' }} />
       </Box>   
    <Box sx={{ display: 'flex', flexDirection: 'column', p:3, flexGrow: 2,marginLeft:'10px',marginRight:'1px'}}>
      
        <Box sx={{marginLeft:'45px' , width :670, marginTop:'-100px'}}>
      <Box sx={{ display: 'flex' , textAlign: 'left' , marginBottom:"10px"}}>
        <Typography  variant="h5" component="h2" gutterBottom>1 Bedroom , 2 Guests</Typography>
        
      </Box>
      <Typography variant="h5" component="h2" align='left' gutterBottom>
      Burj Khalifa View 2 BDR in Burj Royale with Fountain View
      </Typography>
 

      <Typography variant="p" component="p" color="gray" align='left'>
        Welcome to Silkhaus!!!! This property is unique and exclusive, and nothing like you've seen before: it has a balcony with full Burj Khalifa and Fountain view!.This 2 bedroom apartment is located in the brand new Burj Royale in Downtown. It is newly furnished in a modern minimalist style, with unique Eastern design touches. You can walk to The Dubai Mall from the apartment. A perfect place to relax while admiring an amazing view of the Burj Khalifa.
      </Typography>

      <Typography variant="h5" component="h2" align='left' gutterBottom marginTop='20px'>
        Amenties
      </Typography>

    <Grid align='left'>
  <IconButton aria-label="wifi-area">
    <CellWifiIcon/>
  </IconButton>
  <IconButton aria-label="laundry">
    <LocalLaundryServiceIcon/>
  </IconButton>
  <IconButton aria-label="clean">
    <CleaningServicesIcon/>
  </IconButton>
  <IconButton aria-label="kitchen">
    <SoupKitchenIcon/>
  </IconButton>
  </Grid>

      </Box>
      </Box>                     
      </Box>

                                
                            </Grid>
                        </CardContent>
                    </Card>




                    <Card sx={{border: "solid 1px #bbb", marginBottom: "2rem"}}>
                        <CardContent>
                            <Grid container spacing={3} >
                                <Grid item xs={12} sm={5.5} align="left">
                                    <Typography variant="h5" component="h2" gutterBottom>
                                        Check-in date
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray">
                                        {formatDate(booking.start_date)}
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray">
                                        {booking.checkin_time}
                                    </Typography>
                                </Grid>

                                <Grid item xs={false} sm={1} sx={{ display: matchesSM ? 'none' : 'block' }}>
                                    <Divider orientation="vertical" sx={{width:"1px", borderRightWidth: "3px", borderColor: "#bbb"}} />
                                </Grid>
                                
                                <Grid item xs={12} sm={5.5} align={matchesSM ? "left" : "right"}>
                                    <Typography variant="h5" component="h2" gutterBottom>
                                        Check-out date
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray">
                                        {formatDate(booking.end_date)}
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray">
                                        {booking.checkout_time}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                    <Card sx={{border: "solid 1px #bbb", marginBottom: "2rem"}}>
                        <CardContent>
                            <Grid container spacing={3} sx={{borderRightWidth: "3px", borderColor: "#bbb"}}>
                                <Grid item xs={12} sm={5.5} align="left">
                                    <Typography variant="h5" component="h2">
                                        Location
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray" gutterBottom>
                                        <Link component={RouterLink} to={booking.property_details?.property_gmaps_link} target="_blank"> {booking.property_details?.apt_number + ", " + booking.property_details?.building_name + ", " + booking.property_details?.neighbourhood}</Link>
                                    </Typography>

                                    <Typography variant="h5" component="h2">
                                        Apartment Number
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray" gutterBottom>
                                        {booking.property_details?.apt_number}
                                    </Typography>

                                    <Typography variant="h5" component="h2">
                                        Neighbourhood
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray">
                                        {booking.property_details?.neighbourhood}
                                    </Typography>

                                </Grid>

                                <Grid item xs={false} sm={1} sx={{ display: matchesSM ? 'none' : 'block' }}>
                                    <Divider orientation="vertical" sx={{width:"1px", borderRightWidth: "3px", borderColor: "#bbb"}} />
                                </Grid>
                                
                                <Grid item xs={12} sm={5.5} align={matchesSM ? "left" : "right"}>
                                    <Typography variant="h5" component="h2">
                                        Entry Key
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray" gutterBottom>
                                        { booking.status === "ACTIVE" ? (
                                            booking.entry_key ?
                                            (
                                                booking.entry_key
                                            ):
                                            (
                                                "Not added yet"
                                            )
                                        ) : (
                                            "Available after check-in"
                                        )}
                                    </Typography>

                                    <Typography variant="h5" component="h2">
                                        Building name/number
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray" gutterBottom>
                                        {booking.property_details?.building_name}
                                    </Typography>

                                    <Typography variant="h5" component="h2">
                                        Deposit Amount
                                    </Typography>
                                    <Typography variant="p" component="p" color="gray" gutterBottom>
                                        { "AED " + booking.deposit_amount}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                    <Grid container spacing={2} align="center">
                        
                        {/* Show CheckIn button when Booking status UPCOMING */}
                        {booking.status === "UPCOMING" && (
                            <Grid item xs={6} align="center">
								<Button
									onClick={() => customerCheckIn()}
									variant="contained"
									
									sx={{margin:"1rem"}}
									color="primary"
									disabled={showCheckIn}
								>
									Check In
								</Button>
                            </Grid>
                        )}
                        {/* Show CheckOut button when Booking status ACTIVE */}
                        {booking.status === "ACTIVE" && (
                            <Grid item xs={6} align="center">
								<Button
									onClick={() => customerCheckOut()}
									variant="contained"
									
									sx={{margin:"1rem"}}
									color="primary"
								>
									Check Out
								</Button>
                            </Grid>
							)}
                        {/* Show Late Checkout button when Booking status ACTIVE */}
                        { booking.status === "ACTIVE"  &&
                            <Grid item xs={6} align="center">
								<Button margin="normal" variant="contained" disabled={booking.late_request_exist} sx={{margin:"1rem"}} color="primary" onClick={() => setShowLateDateTimeForm(true)}>Request Late Checkout</Button>
							
                            </Grid>
							}
                    </Grid>
                    
                    
                    {/* <Grid container sx={{margin:"20px 0"}}>
                        <Grid item xs={12} sm={12} sx={{marginBottom:"0.2rem"}}>
                            <ItemCard title="Entry Key" description={booking.entry_key || "?"} iconNumber={5} contentRightMargin="5.5rem" singleCard={1} />
                        </Grid>
                    </Grid> */}
                    { booking.late_request && (
                        <>
                            <Typography variant="h4" sx={{my: 3}} >Late Checkout Request</Typography>
                            <LateCheckoutDatagrid lateRequests={[booking.late_request]} isCustomer={true}/>
                        </>
                    )}
                </Container>
                

                <CustomSnackbar message={successMessage} closeSnackbar={()=> setSuccessMessage("")} severity="success" />
                <CustomSnackbar message={errorMessage} closeSnackbar={()=> setErrorMessage("")} severity="error" />
                
                {/* Late CheckOut Request Form */}
                {showLateDateTimeForm && (
                    <Dialog open={showLateDateTimeForm} onClose={handleCancelLateCheckoutButtonClick}>
                        <form onSubmit={handleLateCheckoutButtonClick}>
                        <DialogTitle sx={{ fontWeight: "bold" }}>Late Checkout Request</DialogTitle>
                        <DialogContent>
                            <DialogContentText sx={{ textAlign: "center" }}>Enter late checkout date and time:</DialogContentText>
                            <TextField
                                margin="dense"
                                type="date"
                                name="requested_end_date"
                                fullWidth
                                value={lateDateTime.requested_end_date}
                                onChange={handleLateCheckoutInputChange}
                                required
                            />
                            <TextField
                                margin="dense"
                                type="time"
                                name="requested_checkout_time"
                                fullWidth
                                value={lateDateTime.requested_checkout_time}
                                onChange={handleLateCheckoutInputChange}
                                required
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button type="submit" >Request</Button>
                            <Button onClick={handleCancelLateCheckoutButtonClick}>Cancel</Button>
                        </DialogActions>
                        </form>
                    </Dialog>
                )}
                
        </>
    ) : (
        <div>{error && <CustomErrorBox errorMessage={error} />}</div>
    );
};

export default CustomerBooking;



third waste commit
