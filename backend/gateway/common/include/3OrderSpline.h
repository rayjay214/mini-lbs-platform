#pragma once
class CSpline
{
public:
	CSpline(void);
	~CSpline(void);

//================================================================
// 函数功能： 利用求出的二阶导数求给定点值(结合Spline1,Spline2)
// 输入参数： *xa 为横坐标值，ya为纵坐标值，n为点个数，m为二阶偏导数
//            			  x为给定点，y接收插出来的值
// 返回值：   	  无返回值
//================================================================
void Splint(double *xa,double *ya,double *m,int n,double &x,double &y);

//===========================================================================
// 函数功能： 对一系列点求二阶偏导数，点横坐标单调递增（I型边界）(结合Spline)
// 输入参数： *xa 为横坐标值，ya为纵坐标值，n为点个数，m为二阶偏导数(输出值）
//            			  bound1、bound2为边界点一阶偏导数
// 返回值：   	  无返回值
//===========================================================================
void Spline1(double *xa,double *ya,int n,double *&m,double bound1,double bound2);

//===========================================================================
// 函数功能： 对一系列点求二阶偏导数，点横坐标单调递增（II型边界）(结合Spline)
// 输入参数： *xa 为横坐标值，ya为纵坐标值，n为点个数，m为二阶偏导数(输出值）
//           			  bound1、bound2为边界点二阶偏导数，当bound1和bound2不给值时则使用
//           			  默认值0，即自然边界
// 返回值：   	  无返回值
//===========================================================================
void Spline2(double *xa,double *ya,int n,double *&m,double bound1=0,double bound2=0);
};

